import os
import PIL.ImageGrab
import pyautogui
import win32api
import win32gui
#import win32ui
#from ctypes import windll
import win32con
import numpy
import time
import argparse

import compare_image

def error_exit(des):
    print(des)
    exit(-1)

def grab_screen(left,top,right,bottom):
        return PIL.ImageGrab.grab((left,top,right,bottom))

# this function can grab covered window
# (..  doesn't work for this game)
#def grab_window_image(hwnd,relative_box=None):

#    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
#    width = right - left
#    height = bottom - top

#    hwndDC = win32gui.GetWindowDC(hwnd)
#    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
#    saveDC = mfcDC.CreateCompatibleDC()

#    saveBitMap = win32ui.CreateBitmap()
#    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)

#    saveDC.SelectObject(saveBitMap)

#    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

#    bmpinfo = saveBitMap.GetInfo()
#    bmpstr = saveBitMap.GetBitmapBits(True)

#    im = PIL.Image.frombuffer(
#        'RGB',
#        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
#        bmpstr, 'raw', 'BGRX', 0, 1)

#    win32gui.DeleteObject(saveBitMap.GetHandle())
#    saveDC.DeleteDC()
#    mfcDC.DeleteDC()
#    win32gui.ReleaseDC(hwnd, hwndDC)

#    im.show()
def copy_part_image(image_,left,top,right,bottom):
    return image_.crop((left,top,right,bottom))

def is_empty_grid(image_):
    im = image_
    
    # get center, and resize it smaller
    center = im.resize(size=(int(im.width / 4.0),int(im.height / 4.0)),
                       box=(int(im.width / 4.0),int(im.height / 4.0),
                            int(im.width / 4.0 * 3.0),int(im.height / 4.0 * 3.0)))

    for color in center.getdata():
        if color != (48,76,112):
            return False
    return True
    
def same_grid(image_a,image_b):
    numpy_array_a = numpy.array(image_a)
    numpy_array_b = numpy.array(image_b)
    # no need to resize, it's small enough..
    if 0.95 < compare_image.classify_hist_with_split(numpy_array_a,numpy_array_b,
                                                     size=image_a.size):
        return True
    return False

def game_area_image_to_matrix(image_,
                              grid_width,
                              grid_height):

    # split image into grids
    pos_to_image = {}

    for row in range(11):
        pos_to_image[row] = {}
        for col in range(19):
        
            grid_left = col * grid_width
            grid_top = row * grid_height
            grid_right = grid_left + grid_width
            grid_bottom = grid_top + grid_height

            grid_image = copy_part_image(image_,
                                         grid_left,grid_top,
                                         grid_right,grid_bottom)

            pos_to_image[row][col] = grid_image

    # distinguish grids
    pos_to_type_id = {}

    # empty is 0
    known_type_image = []

    for row in range(11):
        pos_to_type_id[row] = {}
        for col in range(19):
            this_image = pos_to_image[row][col]

            if is_empty_grid(this_image):
                pos_to_type_id[row][col] = 0
                continue

            found = False
            for index in range(len(known_type_image)):
                if same_grid(known_type_image[index],this_image):
                    id = index + 1
                    pos_to_type_id[row][col] = id
                    found = True
                    break

            if not found:
                known_type_image.append(this_image)
                id = len(known_type_image)
                pos_to_type_id[row][col] = id

    return pos_to_type_id

# find first step
def solve_matrix_one_step(matrix):
    matrix_row = len(matrix)
    matrix_col = len(matrix[0])
    for row in range(matrix_row):
        for col in range(matrix_col):
            # can't start from empty
            if matrix[row][col] == 0:
                continue
            target_row,target_col = DFS(row,col,
                                        target_number=matrix[row][col],
                                        empty_number=0,
                                        matrix=matrix,
                                        matrix_row=matrix_row,matrix_col=matrix_col,
                                        path=str(),
                                        first_step=True)
            if target_row:
                return row,col,target_row,target_col

    # solved, or no solution

    for row in range(matrix_row):
        for col in range(matrix_col):
            if matrix[row][col] != 0:
                # no solution
                error_exit('no solution??')
    # all empty, solved
    return None

def in_range(row,col,matrix_row,matrix_col):
    if row < 0\
        or col < 0\
        or row >= matrix_row\
        or col >= matrix_col:
        return False
    return True

def used_lines(path):
    # '0' up
    # '1' right
    # '2' down
    # '3' left
    used_lines = 0
    last_char = 'x' # for start, must be different
    for char in path:
        if char != last_char:
            used_lines+=1
        last_char = char
    return used_lines

# DFS, stop once the path used over 3 lines
def DFS(now_row,now_col,
        target_number,
        empty_number,
        matrix,matrix_row,matrix_col,
        path,
        first_step):

    # first step doesn't check state
    if not first_step:
        # check state

        # check in range
        if not in_range(now_row,now_col,matrix_row,matrix_col):
            return None,None

        # check path used over 3 lines?
        if used_lines(path) > 3:
            return None,None

        # it's graph DFS, but we don't check if we've been here
        # because we can only use at most 3 lines
        # and we don't go back..
        pass

        # check now number
        my_number = matrix[now_row][now_col]
        # found!
        if my_number == target_number:
            return now_row,now_col

        # wrong way..
        # we can only wall on empty
        if my_number != empty_number:
            return None,None

    # check over state
    # now we are on empty grid or start grid

    # go up
    if path == str() or path[-1] != '2':

    # can't go back, if last time we go down...

        new_path = path + '0'
        target_row,target_col = DFS(now_row - 1,now_col,
                                    target_number,
                                    empty_number,
                                    matrix,matrix_row,matrix_col,
                                    new_path,
                                    first_step=False)
        if target_row:
            return target_row,target_col

    # go right
    if path == str() or path[-1] != '3':

    # can't go back, if last time we go left...

        new_path = path + '1'
        target_row,target_col = DFS(now_row,now_col + 1,
                                    target_number,
                                    empty_number,
                                    matrix,matrix_row,matrix_col,
                                    new_path,
                                    first_step=False)
        if target_row:
            return target_row,target_col

    # go down
    if path == str() or path[-1] != '0':

    # can't go back, if last time we go up...

        new_path = path + '2'
        target_row,target_col = DFS(now_row + 1,now_col,
                                    target_number,
                                    empty_number,
                                    matrix,matrix_row,matrix_col,
                                    new_path,
                                    first_step=False)
        if target_row:
            return target_row,target_col

    # go left
    if path == str() or path[-1] != '1':

    # can't go back, if last time we go right...

        new_path = path + '3'
        target_row,target_col = DFS(now_row,now_col - 1,
                                    target_number,
                                    empty_number,
                                    matrix,matrix_row,matrix_col,
                                    new_path,
                                    first_step=False)
        if target_row:
            return target_row,target_col

    # all failed..
    return None,None

def execute_one_step(one_step,
                     game_area_left,game_area_top,
                     grid_width,grid_height):

    from_row,from_col,to_row,to_col = one_step

    from_x = game_area_left + (from_col + 0.5) * grid_width
    from_y = game_area_top + (from_row + 0.5) * grid_height

    to_x = game_area_left + (to_col + 0.5) * grid_width
    to_y = game_area_top + (to_row + 0.5) * grid_height

    pyautogui.moveTo(from_x,from_y)
    pyautogui.click()

    pyautogui.moveTo(to_x,to_y)
    pyautogui.click()

    # hide mouse
    #pyautogui.moveTo(99999999,99999999)
def print_matrix(matrix):
    for row in range(11):
        line = str()
        for col in range(19):
            if matrix[row][col] == 0:
                id = '  '
            else:
                id = '%02d' % matrix[row][col]
            line+='%s  ' % id
        print(line)

if __name__ == '__main__':

    # each step interval for sleep()
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument('--interval',type=float,default=0.0)
    args = arg_parse.parse_args()

    #

    window_title = 'QQ游戏 - 连连看角色版'
    num_grid_per_row = 19
    num_grid_per_col = 11
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)

    #

    hwnd = win32gui.FindWindow(win32con.NULL,window_title)
    if hwnd == 0 :
        error_exit('%s not found' % window_title)

    window_left,window_top,window_right,window_bottom = win32gui.GetWindowRect(hwnd)
    print(window_left,window_top,window_right,window_bottom)
    if min(window_left,window_top) < 0\
        or window_right > screen_width\
        or window_bottom > screen_height:
        error_exit('window is at wrong position')
    window_width = window_right - window_left
    window_height = window_bottom - window_top

    # data is in 800x600 resolution
    game_area_left = window_left + 14.0 / 800.0 * window_width
    game_area_top = window_top + 181.0 / 600.0 * window_height
    game_area_right = window_left + 603 / 800.0 * window_width
    game_area_bottom = window_top + 566 / 600.0 * window_height

    game_area_width = game_area_right - game_area_left
    game_area_height = game_area_bottom - game_area_top
    grid_width = game_area_width / num_grid_per_row
    grid_height = game_area_height / num_grid_per_col 


    # step by step solve problem
    while True:

        print('\n\n\n---------')

        # capture game area image
        game_area_image = grab_screen(game_area_left,game_area_top,
                                      game_area_right,game_area_bottom)

        # get matrix of grid_type_id
        id_matrix = game_area_image_to_matrix(game_area_image,
                                            grid_width,
                                            grid_height)

        # print
        print_matrix(id_matrix)

        # no need to rescan, if we play no-magic-item mode
        while True:

            print('---one step---')
            print_matrix(id_matrix)

            # find one step solution
            one_step = solve_matrix_one_step(id_matrix)
            if not one_step:
                print('solved')
                exit(0)
            print(one_step)
            execute_one_step(one_step,
                             game_area_left,game_area_top,
                             grid_width,grid_height)

            from_row,from_col,to_row,to_col = one_step
            id_matrix[from_row][from_col] = 0
            id_matrix[to_row][to_col] = 0

            time.sleep(args.interval)


