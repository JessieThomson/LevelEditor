import pygame, sys, time, random
from pygame.locals import *
import numpy as np
import math
from tkinter.filedialog import askopenfilename
from tkinter import *
import csv

def DrawRefresh(windowSurface, song_bar_coords, fixed_bar_height, bpm_lines, beat_bar_selected, arrow_pos,
                red_enemies, green_enemies, yellow_enemies, blue_enemies, segment_length):

    BLACK = (0, 0, 0)
    ENEMYGREEN = (0, 255, 0)
    SONGBAR = (63, 61, 75)
    WHITE = (255, 255, 255)
    SELECTEDBAR = (128, 216, 125)
    ENEMYRED = (255, 0, 0)
    ENEMYBLUE = (0, 0, 255)
    ENEMYYELLOW = (230, 255, 0)
    SONGTRACK = (0, 239, 255)

    windowSurface.fill(BLACK)
    pygame.draw.rect(windowSurface, SONGBAR, [song_bar_coords[0], song_bar_coords[1], wanted_bar_length, fixed_bar_height], 0)

    pygame.draw.lines(windowSurface, WHITE, False, [[song_bar_coords[0], song_bar_coords[1] + fixed_bar_height],
                                                    [song_bar_coords[0], song_bar_coords[1] + fixed_bar_height / 2]], 1)

    # pygame.draw.rect(windowSurface, ENEMYGREEN, [450, 30, 50, 50], 0)

    pygame.draw.lines(windowSurface, WHITE, TRUE, [[arrow_pos, song_bar_coords[1]],
                                                   [arrow_pos - 10, song_bar_coords[1] - 10],
                                                   [arrow_pos + 10, song_bar_coords[1] - 10]])
    if not segment_length:
        segment_length = 4

    beat_counter = 0
    for i in range(0, len(bpm_lines)):
        height = song_bar_coords[1] + fixed_bar_height / 2
        if i % (segment_length - 1) == 0:
            # beat_counter += 1
            # if beat_counter == 3:
            height = song_bar_coords[1]
            #     beat_counter = 0
            # else:
            #     height = song_bar_coords[1] + fixed_bar_height / 2

        pygame.draw.lines(windowSurface, WHITE, False,
                          [[song_bar_coords[0] + bpm_lines[i],
                            song_bar_coords[1] + fixed_bar_height],
                           [song_bar_coords[0] + bpm_lines[i], height]], 1)

    if len(beat_bar_selected) > 0:
        pygame.draw.rect(windowSurface, SELECTEDBAR, [song_bar_coords[0] + beat_bar_selected[0], song_bar_coords[1],
                                                      (song_bar_coords[0] + beat_bar_selected[1]) -
                                                      (song_bar_coords[0] + beat_bar_selected[0]), fixed_bar_height], 0)

    for r in red_enemies:
        pygame.draw.circle(windowSurface, ENEMYRED, [int(song_bar_coords[0] + r[1]),
                                                     int(song_bar_coords[1] + enemy_heights[0])], 5)

    for r in green_enemies:
        pygame.draw.circle(windowSurface, ENEMYGREEN, [int(song_bar_coords[0] + r[1]),
                                                       int(song_bar_coords[1] + enemy_heights[1])], 5)

    for r in yellow_enemies:
        pygame.draw.circle(windowSurface, ENEMYYELLOW, [int(song_bar_coords[0] + r[1]),
                                                        int(song_bar_coords[1] + enemy_heights[2])], 5)

    for r in blue_enemies:
        pygame.draw.circle(windowSurface, ENEMYBLUE, [int(song_bar_coords[0] + r[1]),
                                                      int(song_bar_coords[1] + enemy_heights[3])], 5)


def check_collision(mouse_pos, object_pts):
    #     Sort points to the left and right most upper and lower points
    min_x = 100000
    max_x = 0
    min_y = 100000
    max_y = 0
    for p in object_pts:
        if p[0] < min_x:
            min_x = p[0]
        if p[0] > max_x:
            max_x = p[0]
        if p[1] < min_y:
            min_y = p[1]
        if p[1] > max_y:
            max_y = p[1]

    if min_x <= mouse_pos[0] <= max_x and min_y <= mouse_pos[1] <= max_y:
        return TRUE
    else:
        return FALSE


def get_closest_beats(beat_positions, arrow, song_start, song_end):
    # First check which segment the arrow is in
    num_beats = len(beat_positions)
    percentage_through_song = (arrow - song_start)/(song_end - song_start)  # Position is this * song_end + song_start
    position_in_beats = int(percentage_through_song * num_beats)
    closest_beats = []
    if position_in_beats - 2 > 0:
        closest_beats = [beat_positions[x] for x in range(position_in_beats - 2, position_in_beats + 3)]
    else:
        closest_beats = [beat_positions[x] for x in range(0, position_in_beats + 2)]
    return closest_beats


def snap_to_closest(beat_positions, arrow):
    closest_beat = 0
    closest_position = 10000
    for b in beat_positions:
        if abs(b - arrow) < closest_position:
            closest_position = abs(b - arrow)
            closest_beat = b
    return closest_beat


def CalculateBars(segmentLength):
    bpm_lines = []
    bpm_lines += [0]
    current_max = 0.0
    beat_bar = [[0]]
    count = 1
    all_beats_in_song = segmentLength * beats_in_song
    example_bpm = wanted_bar_length / all_beats_in_song
    while current_max < wanted_bar_length:
        current_max = bpm_lines[len(bpm_lines) - 1] + example_bpm
        bpm_lines += [current_max]
        if count % (segmentLength - 1) == 0:
            beat_bar[len(beat_bar) - 1] += [bpm_lines[len(bpm_lines) - 1]]
            beat_bar += [[bpm_lines[len(bpm_lines) - 1]]]
        count += 1
    return bpm_lines, beat_bar

def CheckIfEmpty(list):
    if len(list) <= 0:
        list = [[0, 0, "0"]]

    return list

def SaveCSV(red_enemies, green_enemies, blue_enemies, yellow_enemies):
    # Concatenate all enemies into one list of times and enemy type to write out
    # Remove all duplicate enemies in lists
    red_enemies = CheckIfEmpty(red_enemies)
    blue_enemies = CheckIfEmpty(blue_enemies)
    green_enemies = CheckIfEmpty(green_enemies)
    yellow_enemies = CheckIfEmpty(yellow_enemies)

    all_enemies = np.array(np.concatenate((red_enemies, green_enemies, blue_enemies, yellow_enemies)))
    unique_a = np.unique(all_enemies.view([('', all_enemies.dtype)] * all_enemies.shape[1]))
    final_list = unique_a.view(all_enemies.dtype).reshape((unique_a.shape[0], all_enemies.shape[1]))
    enemy_indices = [float(x) for x in final_list[:, 0]]
    ind = np.argsort(enemy_indices)
    final_list = final_list[ind, :]

    # print(final_list)
    seconds_per_beat = float(song_size / (len(bpm_lines)-1))
    print(len(bpm_lines), song_size)
    with open('level.csv', 'w', newline='') as csvfile:
        fieldnames = ['SectionType', 'Required Intensity', 'Enemy Type', 'Move Speed',
                      'Beat Division', 'Second', 'BAR', 'BEAT']
        writer = csv.writer(csvfile)
        writer.writerow(['BPM', beats_in_song])
        writer.writerow(['Beat Divisions', segment])
        writer.writerow(['Seconds Per Beat', seconds_per_beat])
        for i in range(15-3):
            writer.writerow({'Metadata'})
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        move_speed = 5
        section_type = 'Wave'
        writer.writeheader()
        curr_seg = 1
        prev_seg = 0
        curr_beat_count = 1
        curr_bar_count = 1
        curr_beat = 1
        curr_bar = 1
        enemy_type = ""
        for line in bpm_lines:
            if curr_beat_count % 4 == 0 and curr_seg % segment == 0:
                curr_bar_count += 1
                curr_bar = curr_bar_count
            else:
                curr_bar = " "

            if (curr_seg - prev_seg) / segment >= 1 and prev_seg is not curr_seg:
                prev_seg = curr_seg
                curr_beat_count += 1
                if curr_beat_count > 4:
                    curr_beat_count = 1
                curr_beat = curr_beat_count
            else:
                curr_beat = " "

            if curr_seg is 1 and prev_seg is not curr_seg:
                curr_beat = 1
                curr_bar = 1

            ii = np.where(final_list[:, 1] == str(line))[0]
            if len(ii) <= 0:
                enemy_type = "None"
                writer.writerow({'SectionType': section_type, 'Required Intensity': '0', 'Enemy Type': enemy_type,
                                 'Move Speed': move_speed, 'Beat Division': curr_seg,
                                 'Second': str((line / wanted_bar_length) * song_size),
                                 'BAR': curr_bar, 'BEAT': curr_beat})
            else:
                for r in final_list[ii]:
                    if r[2] == "red":
                        enemy_type = "Thrower"
                    elif r[2] == "green":
                        enemy_type = "Leaper"
                    elif r[2] == "yellow":
                        enemy_type = "Grunt"
                    elif r[2] == "blue":
                        enemy_type = "Charger"
                    else:
                        enemy_type = "None"

                    writer.writerow({'SectionType': section_type, 'Required Intensity': '0', 'Enemy Type': enemy_type,
                                     'Move Speed': move_speed, 'Beat Division': curr_seg,
                                     'Second': str((line / wanted_bar_length) * song_size),
                                     'BAR': curr_bar, 'BEAT': curr_beat})

            curr_seg += 1



import GameStuff.bpm_detector as bpm_detect
import GameStuff.InputBox as InputBox
import GameStuff.Pane as Pane
from pydub import AudioSegment

if __name__ == '__main__':
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    pygame.mixer.init()
    # Load song file using Tk - best to use Mp3 version of the song to reduce white noise when converting
    sound_file = ""
    root = Tk()
    sound_file = askopenfilename()
    root.destroy()
    print(sound_file)

    song_size = 0
    # Because the bpm needs a 16bit wav file...
    wav_file = None
    if sound_file is not "":
        # If the file is not an ogg file, convert it
        extension = str(sound_file).split(".")[1]
        if extension is "wav":
            wav_file = sound_file
        else:
            song = AudioSegment.from_file(sound_file, extension)
            split_files = str(sound_file).split("/")
            wav_file = '/'.join(split_files[:-1])
            wav_file = wav_file + "/" + str(split_files[len(split_files) - 1]).split(".")[0] + ".wav"
            wav_file = wav_file
            song.export(wav_file, format="wav")
        print(extension)
        if extension is not "ogg":
            song = AudioSegment.from_file(sound_file, extension)
            split_files = str(sound_file).split("/")
            ogg_file = '/'.join(split_files[:-1])
            ogg_file = ogg_file + "/" + str(split_files[len(split_files) - 1]).split(".")[0] + ".ogg"
            sound_file = ogg_file
            song.export(ogg_file, format="ogg")

        a = pygame.mixer.Sound(sound_file)
        song_size = a.get_length()
        print("length", song_size)
        pygame.mixer.music.load(sound_file)

    windowWidth = 1700
    windowHeight = 900
    windowSurface = pygame.display.set_mode((windowWidth, windowHeight), 0, 32)
    pygame.display.set_caption("LevelEditor")
    segment_input = InputBox.InputBox(130, 100, 140, 32, "4")
    segment_label = Pane.Pane(0, 100, 'white', "Segments: ")
    # get screen size
    info = pygame.display.Info()
    sw = info.current_w
    sh = info.current_h
    wanted_bar_length = float(windowWidth * 0.9)
    fixed_bar_height = float(windowHeight * 0.4)
    print("Bar size", wanted_bar_length, fixed_bar_height)
    # Set enemy bar heights to draw at
    enemy_heights = []
    for i in range(4):
        enemy_heights += [(0.20 * (i+1)) * fixed_bar_height]

    # BPM detector
    beats_in_song = bpm_detect.run(wav_file)  # 40.0
    BPM_label = Pane.Pane(0, 60, 'white', "BPM: " + str(beats_in_song))

    # Enemy labels
    red_label = Pane.Pane(sw - 300, 60, 'red', "Red enemies: 0")
    green_label = Pane.Pane(sw - 300, 90, 'green', "Green enemies: 0")
    yellow_label = Pane.Pane(sw - 300, 120, 'yellow', "Yellow enemies: 0")
    blue_label = Pane.Pane(sw - 300, 150, 'blue', "Blue enemies: 0")

    minutes = song_size / 60
    seconds = int(minutes % 1 * 60)
    print("song length in hh:mm:ss - 00:", int(minutes), ":", seconds)
    # all_beats_in_song = int(minutes) * beats_in_song + int((seconds / 60) * beats_in_song)
    # print(all_beats_in_song)
    # example_bpm = song_size / beats_in_song
    # example_bpm = wanted_bar_length / all_beats_in_song
    beat_bar_selected = []
    song_bar_coords = [sw / 2 - wanted_bar_length / 2, 340]
    red_enemy_positions = []
    blue_enemy_positions = []
    yellow_enemy_positions = []
    green_enemy_positions = []

    arrow_pos = song_bar_coords[0]
    beat_bar = [[0]]
    bpm_lines = []
    segment = 4
    bpm_lines, beat_bar = CalculateBars(segment)

    play = FALSE
    playing = FALSE
    drag_arrow = FALSE
    song_time = 0
    song_offset = song_bar_coords[0]

    # Joystick initialisation
    joysticks_present = FALSE
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    if joysticks:
        joysticks_present = TRUE
        joystick = joysticks[0]
        joystick.init()
    while True:
        # Play, pause and scrub along song
        if playing:
            play_time = pygame.mixer.music.get_pos() / 1000
            if play_time < 0:
                play = FALSE
                playing = FALSE
            else:
                arrow_pos = song_offset + (play_time / song_size) * wanted_bar_length
                song_time = song_time + play_time
        if play and playing is FALSE:
            pygame.mixer.music.unpause()
            playing = TRUE
        if drag_arrow:
            mousex, mousey = pygame.mouse.get_pos()
            arrow_pos = mousex
            song_time = ((mousex - song_bar_coords[0]) / wanted_bar_length) * song_size
            song_offset = mousex
            # Need to put a check in to make sure the time doesn't go past 0 or the length of the song
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # Check the input text box events
            value = segment_input.handle_event(event)
            if value:
                segment = value
                bpm_lines, beat_bar = CalculateBars(segment)

            #################################################################
            # Check all keyboard presses
            if event.type == pygame.KEYDOWN:
                # Reset song to the start
                if event.key == pygame.K_BACKSPACE:
                    playing = FALSE
                    play = FALSE
                    song_time = 0
                    pygame.mixer.music.play(0, 0)
                    pygame.mixer.music.pause()
                    arrow_pos = song_bar_coords[0]
                    song_offset = song_bar_coords[0]
                # Save current csv
                if event.key == pygame.K_s:
                    SaveCSV(red_enemy_positions, green_enemy_positions, blue_enemy_positions, yellow_enemy_positions)
                # Play pause song
                if event.key == pygame.K_p:
                    if song_time/1000 < song_size:
                        if play is FALSE:
                            pygame.mixer.music.play(0, song_time)
                        else:
                            song_offset = arrow_pos
                            playing = FALSE
                        pygame.mixer.music.pause()
                        play = TRUE if play is FALSE else FALSE
            #################################################################
            # Check all joystick buttons
            if joysticks_present:
                if event.type == pygame.JOYBUTTONDOWN:
                    position = get_closest_beats(bpm_lines, arrow_pos, song_bar_coords[0],
                                                 song_bar_coords[0] + wanted_bar_length)

                    closest_song_bar = snap_to_closest(position, arrow_pos - song_bar_coords[0])
                    nearest_pos = closest_song_bar
                    closest_song_bar = (closest_song_bar / wanted_bar_length) * song_size
                    if joystick.get_button(0) > 0:
                        if [closest_song_bar, nearest_pos, 'green'] not in green_enemy_positions:
                            green_enemy_positions += [[closest_song_bar, nearest_pos, 'green']]
                        green_label.update("Green enemies: " + str(len(green_enemy_positions)))
                    if joystick.get_button(1) > 0:
                        if [closest_song_bar, nearest_pos, 'red'] not in red_enemy_positions:
                            red_enemy_positions += [[closest_song_bar, nearest_pos, 'red']]
                        red_label.update("Red enemies: " + str(len(red_enemy_positions)))
                    if joystick.get_button(2) > 0:
                        if [closest_song_bar, nearest_pos, 'blue'] not in blue_enemy_positions:
                            blue_enemy_positions += [[closest_song_bar, nearest_pos, 'blue']]
                        blue_label.update("Blue enemies: " + str(len(blue_enemy_positions)))
                    if joystick.get_button(3) > 0:
                        if [closest_song_bar, nearest_pos, 'yellow'] not in yellow_enemy_positions:
                            yellow_enemy_positions += [[closest_song_bar, nearest_pos, 'yellow']]
                        yellow_label.update("Yellow enemies: " + str(len(yellow_enemy_positions)))
            #################################################################
            # Check all mouse buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousex, mousey = pygame.mouse.get_pos()
                # Select beat
                if (song_bar_coords[0] <= mousex < song_bar_coords[0] + wanted_bar_length)\
                        and (song_bar_coords[1] <= mousey < song_bar_coords[1] + fixed_bar_height):
                    bar_count = 0
                    for bar in beat_bar:
                        if bar[0] + song_bar_coords[0] < mousex < bar[1] + song_bar_coords[0]:
                            beat_bar_selected = bar
                        bar_count += 1
                # Select and drag arrow
                elif drag_arrow is not TRUE:
                    if check_collision([mousex, mousey], [[arrow_pos, song_bar_coords[1]],
                                                   [arrow_pos - 10, song_bar_coords[1] - 10],
                                                   [arrow_pos + 10, song_bar_coords[1] - 10]]):
                        drag_arrow = TRUE
            # Reset drag
            if event.type == pygame.MOUSEBUTTONUP:
                if drag_arrow:
                    drag_arrow = FALSE
        segment_input.update()
        DrawRefresh(windowSurface, song_bar_coords, fixed_bar_height, bpm_lines, beat_bar_selected, arrow_pos,
                    red_enemy_positions, green_enemy_positions, yellow_enemy_positions, blue_enemy_positions, segment)

        segment_input.draw(windowSurface)
        segment_label.draw(windowSurface)
        BPM_label.draw(windowSurface)
        red_label.draw(windowSurface)
        green_label.draw(windowSurface)
        yellow_label.draw(windowSurface)
        blue_label.draw(windowSurface)
        pygame.time.Clock().tick(100)

        pygame.display.update()
