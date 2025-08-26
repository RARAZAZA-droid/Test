import PySimpleGUI as sg
import time
import serial as ser
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import numpy as np

# Set modern theme for PySimpleGUI
sg.theme('DarkBlue3')

# Modern color scheme
COLORS = {
    'primary': '#1e3a8a',      # Deep blue
    'secondary': '#3b82f6',    # Bright blue
    'accent': '#06d6a0',       # Teal green
    'warning': '#f59e0b',      # Amber
    'danger': '#ef4444',       # Red
    'success': '#10b981',      # Emerald
    'background': '#f8fafc',   # Light gray
    'surface': '#ffffff',      # White
    'text_primary': '#1f2937', # Dark gray
    'text_secondary': '#6b7280' # Medium gray
}

light_epsilon = 0.3
object_light_epsilon = 0.3


# def objects_detector():
#     layout = [
#         [sg.Text("Enter Masking Distance [cm]:", text_color='#000000', background_color='#9AF1FF',
#                  font=('Segoe UI', 10)),
#          sg.InputText(key="-DISTANCE-", size=(20, 1))],
#         [sg.Button("Start Objects Scan", key="-SCAN-", button_color='#000000'),
#          sg.Button("Back", key="-BACK-", button_color='#000000')],
#         [sg.Output(key="-OUTPUT-", size=(45, 5))]
#     ]
#     window = sg.Window("Objects Detector System", layout, background_color='#9AF1FF', font=('Segoe UI', 10),
#                        resizable=True, return_keyboard_events=True, finalize=True)
#     window.bind("<Escape>", "-ESCAPE-")

#     while True:
#         event, values = window.read()
#         if event in (sg.WINDOW_CLOSED, "-BACK-", "-ESCAPE-"):
#             send_command('0')
#             break
#         elif event == "-SCAN-" or event == '\r':
#             window["-SCAN-"].update(disabled=True)
#             window["-BACK-"].update(disabled=True)
#             distance_arr = []
#             masking_distance = values["-DISTANCE-"]
#             send_command('S')
#             angle1 = int(receive_data())
#             angle2 = int(receive_data())
#             counter = 0
#             while True:
#                 window.refresh()
#                 distance = int(receive_data())
#                 if distance == 999:
#                     break
#                 if counter > 4:  # Servo stuck at around first 12 samples
#                     if distance < int(masking_distance):
#                         distance_arr.append(distance)
#                         window['-OUTPUT-'].update(f"Distance: {'{:>3}'.format(distance)} [cm]\n", append=True)
#                     else:
#                         window['-OUTPUT-'].update(f"Distance: {'{:>3}'.format(distance)} [cm]", append=True)
#                         window['-OUTPUT-'].Widget.tag_configure("red_text", foreground="red")
#                         window['-OUTPUT-'].Widget.insert("end", " - MASKED\n", "red_text")
#                         distance_arr.append(0)
#                 counter += 1

#             degree_arr = [round(float(5) + i * (float(180) - float(0)) / (len(distance_arr) - 1), 1)
#                           for i in range(len(distance_arr))]
#             window['-OUTPUT-'].update(f"Distance array: {distance_arr}\n", append=True)
#             window['-OUTPUT-'].update(f"Degree array: {degree_arr}\n", append=True)
#             draw_scanner_map(distance_arr, degree_arr)
#             window["-SCAN-"].update(disabled=False)
#             window["-BACK-"].update(disabled=False)

# def objects_detector():

# #TODO : adjust the angels of the servo motor(step_size).fix the plot

#     layout = [
#         [sg.Text("Enter Masking Distance [cm]:", text_color='#000000', background_color='#9AF1FF',
#                  font=('Segoe UI', 10)),
#          sg.InputText(key="-DISTANCE-", size=(20, 1))],
#         [sg.Button("Start Objects Scan", key="-SCAN-", button_color='#000000'),
#          sg.Button("Back", key="-BACK-", button_color='#000000')],
#         [sg.Output(key="-OUTPUT-", size=(45, 5))]
#     ]
#     window = sg.Window("Objects Detector System", layout, background_color='#9AF1FF', font=('Segoe UI', 10),
#                        resizable=True, return_keyboard_events=True, finalize=True)
#     window.bind("<Escape>", "-ESCAPE-")

#     while True:
#         event, values = window.read()
#         if event in (sg.WINDOW_CLOSED, "-BACK-", "-ESCAPE-"):
#             send_command('0')
#             break
#         elif event == "-SCAN-" or event == '\r':
#             window["-SCAN-"].update(disabled=True)
#             window["-BACK-"].update(disabled=True)
           
#             masking_distance = values["-DISTANCE-"]
#             send_command('S')
#             # angle1 = int(receive_data())
#             # angle2 = int(receive_data())
#             counter = 0 # step for counting bad beggining
#             steps_counter = 0 # counting how many degrees for
#             r = 0
#             while True:
#                 window.refresh()
#                 distance = int(receive_data())
#                 if distance == 999:
#                     break
#                 if counter > 10:  # Servo stuck at around first 12 samples
#                     if distance < int(masking_distance):
#                         if steps_counter == 0:
#                             distance_arr.append(distance)
#                             r = distance
#                         else:
#                             distance_arr.append(0)   
#                         steps_counter += 1
#                         window['-OUTPUT-'].update(f"Distance: {'{:>3}'.format(distance)} [cm] Angle {'{:>3}'.format(counter * step_size )}\n", append=True)

#                     elif distance > int(masking_distance):
#                         if steps_counter != 0:
#                             d_phi = steps_counter * step_size - float(40)      # 1 is the step size in deg, 40 is for sensor detection angle correction
#                             l = r * math.sin(math.radians(d_phi)) 
#                             l_arr.append(l)
#                             steps_counter = 0 
#                             window['-OUTPUT-'].update(f"Distance: {'{:>3}'.format(distance)} [cm] Angle {'{:>3}'.format(counter * step_size )}", append=True)
#                             window['-OUTPUT-'].Widget.tag_configure("red_text", foreground="red")
#                             window['-OUTPUT-'].Widget.insert("end", " - MASKED\n", "red_text")
                            

#                             distance_arr.append(0)

#                         else:

#                             window['-OUTPUT-'].update(f"Distance: {'{:>3}'.format(distance)} [cm] Angle {'{:>3}'.format(counter * step_size )}", append=True)
#                             window['-OUTPUT-'].Widget.tag_configure("red_text", foreground="red")
#                             window['-OUTPUT-'].Widget.insert("end", " - MASKED\n", "red_text")
#                             distance_arr.append(0)
                
                        
#                 counter += 1
#             print(f"width {l_arr}")
#             degree_arr = [round(step_size + i * (float(180) - float(0)) / (len(distance_arr) - 1), 1)
#                           for i in range(len(distance_arr))]
#             window['-OUTPUT-'].update(f"Distance array: {distance_arr}\n", append=True)
#             window['-OUTPUT-'].update(f"Degree array: {degree_arr}\n", append=True)
#             draw_scanner_map(distance_arr, degree_arr,l_arr)
#             window["-SCAN-"].update(disabled=False)
#             window["-BACK-"].update(disabled=False)
#     window.close()


def objects_detector():
    layout = [
        [sg.Text("🎯 Object Detection System", font=('Segoe UI', 18, 'bold'), 
                 text_color=COLORS['primary'], justification='center', expand_x=True, pad=(0, 20))],
        [sg.Frame('Configuration', [
            [sg.Text("Masking Distance [cm]:", font=('Segoe UI', 12), text_color=COLORS['text_primary']),
             sg.Push(),
             sg.InputText(key="-DISTANCE-", size=(15, 1), font=('Segoe UI', 12), 
                         border_width=2, pad=(10, 0))]
        ], font=('Segoe UI', 12, 'bold'), title_color=COLORS['secondary'], 
           border_width=2, relief='solid', pad=(20, 15))],
        [sg.VPush()],
        [sg.Button("🔍 Start Objects Scan", key="-SCAN-", size=(20, 2), 
                   font=('Segoe UI', 12, 'bold'), button_color=(COLORS['surface'], COLORS['success']),
                   border_width=0, pad=(10, 10)),
         sg.Push(),
         sg.Button("← Back", key="-BACK-", size=(12, 2), 
                   font=('Segoe UI', 12), button_color=(COLORS['surface'], COLORS['text_secondary']),
                   border_width=0, pad=(10, 10))],
        [sg.VPush()],
        [sg.Frame('Scan Results', [
            [sg.Output(key="-OUTPUT-", size=(60, 12), font=('Consolas', 10), 
                      text_color=COLORS['text_primary'], background_color=COLORS['surface'])]
        ], font=('Segoe UI', 12, 'bold'), title_color=COLORS['secondary'], 
           border_width=2, relief='solid', pad=(20, 15), expand_x=True)]
    ]
    window = sg.Window("Objects Detector System", layout, size=(800, 700), 
                       resizable=True, return_keyboard_events=True, finalize=True,
                       element_justification='center', margins=(30, 30))
    window.bind("<Escape>", "-ESCAPE-")

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "-BACK-", "-ESCAPE-"):
            send_command('0')
            break
        elif event == "-SCAN-" or event == '\r':
            window["-SCAN-"].update(disabled=True)
            window["-BACK-"].update(disabled=True)
           
            masking_distance = values["-DISTANCE-"]
            send_command('S')
            counter = 0 # step for counting bad beggining
            distance_arr = []
            step_size = int(1)
            while True:
                window.refresh()
                distance = int(receive_data())

                if distance == 999:
                    break

                if counter > -1:  # Servo stuck at around first 12 samples
                    distance_arr.append(distance)

                    window['-OUTPUT-'].update(f"Distance: {'{:>3}'.format(distance)} [cm] Angle {'{:>3}'.format(counter * step_size )}\n", append=True)
                    if distance > int(masking_distance):
                        window['-OUTPUT-'].Widget.tag_configure("red_text", foreground="red")
                        window['-OUTPUT-'].Widget.insert("end", " - MASKED\n", "red_text")

                counter += 1

            degree_arr = [i for i in range(len(distance_arr))]
            res = calc_width(distance_arr,10,int(masking_distance))
                     
            width_arr = [0] * len(distance_arr)
            pos_arr = []
            for pair in res:
                start_angle = pair[0]
                d_phi = pair[-1] 
                center_ratio = get_distance_ratio(distance)
                d_phi_norm = d_phi * center_ratio  # correction factor
                width_arr[start_angle] = distance_arr[start_angle] * math.sin(math.radians(d_phi_norm))
                pos_arr.append((distance_arr[start_angle],start_angle + d_phi//2,width_arr[start_angle]))

            window['-OUTPUT-'].update(f"Distance array: {distance_arr}\n", append=True)
            window['-OUTPUT-'].update(f"Degree array: {degree_arr}\n", append=True)

            print(f"WOWO{res} {width_arr}")
            print(f"ELEMENTS{pos_arr}")
            draw_scanner_map(pos_arr)
            window["-SCAN-"].update(disabled=False)
            window["-BACK-"].update(disabled=False)
    window.close()


def calc_width(distance_arr, d, masking_num):
    n = len(distance_arr)
    results = []
    i = 0

    # Mask elements in place
    for idx in range(n):
        if distance_arr[idx] > masking_num:
            distance_arr[idx] = 0

    while i < n:
        # Skip zeros
        if distance_arr[i] == 0:
            i += 1
            continue

        start = i
        min_val = distance_arr[i]
        max_val = distance_arr[i]
        j = i + 1

        while j < n and distance_arr[j] != 0:
            min_val = min(min_val, distance_arr[j])
            max_val = max(max_val, distance_arr[j])
            if max_val - min_val > d:
                break
            j += 1

        length = j - start
        if length > 5:
            results.append((start, length))

        i = j  # move to the next non-overlapping section

    return results

def get_distance_ratio(distance):
    if distance <= 60:
        return 0.25  # Use 25% for close objects
    elif distance <= 100:
        return 0.15  # Use 15% for medium distance
    else:
        return 0.10  # Use only 10% for far objects

def telemeter():
    #  angle = 0
    dynamic_flag = 0

    layout = [
        [sg.Text("📐 Telemeter System", font=('Segoe UI', 18, 'bold'), 
                 text_color=COLORS['primary'], justification='center', expand_x=True, pad=(0, 20))],
        [sg.Frame('Angle Configuration', [
            [sg.Text("Target Angle [0° - 180°]:", font=('Segoe UI', 12), text_color=COLORS['text_primary']),
             sg.Push(),
             sg.InputText(key="-ANGLE-", size=(15, 1), font=('Segoe UI', 12), 
                         border_width=2, pad=(10, 0), justification='center')]
        ], font=('Segoe UI', 12, 'bold'), title_color=COLORS['secondary'], 
           border_width=2, relief='solid', pad=(20, 15))],
        [sg.VPush()],
        [sg.Button("▶️ Start Measure", key="-START-", size=(15, 2), 
                   font=('Segoe UI', 12, 'bold'), button_color=(COLORS['surface'], COLORS['success']),
                   border_width=0, pad=(10, 10)),
         sg.Button("⏹️ Stop Measure", key="-STOP-", size=(15, 2), 
                   font=('Segoe UI', 12, 'bold'), button_color=(COLORS['surface'], COLORS['danger']),
                   border_width=0, pad=(10, 10), disabled=True),
         sg.Push(),
         sg.Button("← Back", key="-BACK-", size=(12, 2), 
                   font=('Segoe UI', 12), button_color=(COLORS['surface'], COLORS['text_secondary']),
                   border_width=0, pad=(10, 10))],
        [sg.VPush()],
        [sg.Frame('Measurement Results', [
            [sg.Output(key="-OUTPUT-", size=(60, 8), font=('Consolas', 11), 
                      text_color=COLORS['text_primary'], background_color=COLORS['surface'])]
        ], font=('Segoe UI', 12, 'bold'), title_color=COLORS['secondary'], 
           border_width=2, relief='solid', pad=(20, 15), expand_x=True)]
    ]

    window = sg.Window("Telemeter", layout, size=(750, 600), resizable=True,
                       return_keyboard_events=True, finalize=True,
                       element_justification='center', margins=(30, 30))
    window.bind("<Escape>", "-ESCAPE-")

    while True:
        window.refresh()
        event, values = window.read(timeout=100)
        if event in (sg.WINDOW_CLOSED, "-BACK-", "-ESCAPE-"):
            send_command('0')
            break
        elif event == "-START-" or event == '\r':

            window["-START-"].update(disabled=True)
            window["-BACK-"].update(disabled=True)
            window["-STOP-"].update(disabled=False)
            print("Performing Ultrasonic Scan")
            window.refresh()
            send_command('T')
            angle = int(values["-ANGLE-"])
            dynamic_flag = 1
            send_angle(angle)

        elif event == "-STOP-":
            window["-STOP-"].update(disabled=True)
            window["-START-"].update(disabled=False)
            window["-BACK-"].update(disabled=False)
            window.refresh()
            send_command('M')
            dynamic_flag = 0

        elif event == "__TIMEOUT__":
            if dynamic_flag:
                distance = int(receive_data())
                angle = int(receive_data())
                window['-OUTPUT-'].update(f"Distance: {'{:>3}'.format(distance)} [cm] ", append=True)
                window['-OUTPUT-'].update(f"| Angle: {'{:>3}'.format(angle)} [°]\n", append=True)
    window.close()


def lights_detector():
    layout = [
        [sg.Text("💡 Light Sources Detector", font=('Segoe UI', 18, 'bold'), 
                 text_color=COLORS['primary'], justification='center', expand_x=True, pad=(0, 20))],
        [sg.Frame('Actions', [
            [sg.Button("🔍 Start Light Sources Scan", key="-SCAN-", size=(25, 2), 
                       font=('Segoe UI', 12, 'bold'), button_color=(COLORS['surface'], COLORS['warning']),
                       border_width=0, pad=(10, 10))],
            [sg.Button("⚙️ Calibrate Using PB0", key="-CALIBRATE-", size=(25, 2), 
                       font=('Segoe UI', 12, 'bold'), button_color=(COLORS['surface'], COLORS['accent']),
                       border_width=0, pad=(10, 10))],
            [sg.Button("← Back", key="-BACK-", size=(25, 2), 
                       font=('Segoe UI', 12), button_color=(COLORS['surface'], COLORS['text_secondary']),
                       border_width=0, pad=(10, 10))]
        ], font=('Segoe UI', 12, 'bold'), title_color=COLORS['secondary'], 
           border_width=2, relief='solid', pad=(20, 15), element_justification='center')],
        [sg.VPush()],
        [sg.Frame('Calibration Progress', [
            [sg.ProgressBar(10, orientation='h', expand_x=True, size=(50, 25), 
                           bar_color=(COLORS['warning'], COLORS['background']), key='-PBAR-',
                           border_width=2, relief='solid')],
            [sg.Text('Ready to calibrate', key='-OUT-', font=('Segoe UI', 12), 
                     text_color=COLORS['text_primary'], justification='center', expand_x=True, pad=(0, 10))]
        ], font=('Segoe UI', 12, 'bold'), title_color=COLORS['secondary'], 
           border_width=2, relief='solid', pad=(20, 15))],
        [sg.VPush()],
        [sg.Frame('Detection Results', [
            [sg.Output(key="-OUTPUT-", size=(80, 10), font=('Consolas', 10), 
                      text_color=COLORS['text_primary'], background_color=COLORS['surface'])]
        ], font=('Segoe UI', 12, 'bold'), title_color=COLORS['secondary'], 
           border_width=2, relief='solid', pad=(20, 15), expand_x=True)]
    ]
    window = sg.Window("Light Sources Detector System", layout, size=(900, 750),
                       resizable=True, return_keyboard_events=True, finalize=True,
                       element_justification='center', margins=(30, 30))
    window.bind("<Escape>", "-ESCAPE-")

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, "-BACK-", "-ESCAPE-"):
            send_command('0')
            break
        elif event == "-CALIBRATE-":
            LDR_calibrate_arr = []
            window["-BACK-"].update(disabled=True)
            window["-SCAN-"].update(disabled=True)
            window["-CALIBRATE-"].update(disabled=True)
            window["-CALIBRATE-"].update("Press PB0 to calibrate")
            window['-PBAR-'].update(current_count=0)
            window['-OUT-'].update("")
            send_command('L')

            for i in range(10):
                window.refresh()
                window['-OUTPUT-'].update(f"Please Press Push Button 0 to take a sample: {i + 1}\n", append=True)
                LDR1_val = int(receive_data()) / 292
                LDR2_val = int(receive_data()) / 292
                LDR1_val_trunc = "%.2f" % LDR1_val
                LDR2_val_trunc = "%.2f" % LDR2_val
                LDRavg_val_trunc = "%.2f" % ((LDR1_val + LDR2_val) / 2)

                window['-OUTPUT-'].update(
                    f"Left LDR value: {LDR1_val_trunc} [V]| Right LDR value: {LDR2_val_trunc} [V]\n", append=True)
                window['-OUTPUT-'].update(f"Average value: {LDRavg_val_trunc} [V]\n", append=True)

                LDR_calibrate_arr.append((LDR1_val + LDR2_val) / 2)

                window['-PBAR-'].update(current_count=i + 1)
                window['-OUT-'].update(f"sample {i + 1} received")
                time.sleep(0.05)

            window["-BACK-"].update(disabled=False)
            window["-SCAN-"].update(disabled=False)
            window["-CALIBRATE-"].update("Done Calibrating!")
            window['-PBAR-'].update(current_count=0)

            expanded_LDR_calibrate_arr = expand_calibration_array(LDR_calibrate_arr, 50)
            save_calibration_values(expanded_LDR_calibrate_arr)

        elif event == "-SCAN-" or event == '\r':
            window["-BACK-"].update(disabled=True)
            window["-SCAN-"].update(disabled=True)
            window["-CALIBRATE-"].update(disabled=True)
            distance_arr = []
            masking_distance = 49
            send_command('K')
            angle1 = int(receive_data())
            angle2 = int(receive_data())
            counter = 0
            flag = 0
            while True:
                window.refresh()
                arr = measure_two_ldr_samples()
                if counter > 8:  # Servo stuck at around first 12 samples
                    light_distance = arr[0] + 1
                    ldr_val1 = arr[1]
                    ldr_val2 = arr[2]
                    if light_distance == 0:
                        break

                    LDR1_val_trunc = "%.2f" % ldr_val1
                    LDR2_val_trunc = "%.2f" % ldr_val2
                    window['-OUTPUT-'].update(
                        f"Left LDR value: {LDR1_val_trunc} [V] | Right LDR value: {LDR2_val_trunc} [V]", append=True)

                    window['-OUTPUT-'].update(f" | Estimate Distance: {light_distance} [cm]", append=True)
                    if abs(ldr_val1 - ldr_val2) < 99999 and ldr_val1 < 3 and ldr_val2 < 3:  
                    # first condition the object should be infront , the later cond ,above those values the light is not a source just noies 
                        if light_distance > int(masking_distance):
                            window['-OUTPUT-'].Widget.tag_configure("red_text", foreground="red")
                            window['-OUTPUT-'].Widget.insert("end", " (MASKED) \n", "red_text")
                            distance_arr.append(0)
                            flag = 0
                        else:

                            window['-OUTPUT-'].Widget.tag_configure("green_text", foreground="green")
                            window['-OUTPUT-'].Widget.insert("end", " - LIGHT DETECTED \n", "green_text")
                            if flag == 1:
                                distance_arr.append(light_distance)
                            else:
                                distance_arr.append(0)
                            flag = 1
                    else:
                        flag = 0
                        window['-OUTPUT-'].Widget.tag_configure("red_text", foreground="red")
                        window['-OUTPUT-'].Widget.insert("end", " (NOISE) \n", "red_text")
                        distance_arr.append(0)
                counter += 1

            degree_arr = [round(float(5) + i * (float(180) - float(0)) / (len(distance_arr) - 1), 1)
                          for i in range(len(distance_arr))]

            window['-OUTPUT-'].update(f"Distance array: {distance_arr}\n", append=True)
            window['-OUTPUT-'].update(f"Degree array: {degree_arr}\n", append=True)

            draw_scanner_map_lights(distance_arr, distance_arr, degree_arr)
            window["-BACK-"].update(disabled=False)
            window["-SCAN-"].update(disabled=False)
            window["-CALIBRATE-"].update(disabled=False)

    window.close()


def light_objects_detector():
    layout = [
        [sg.Text("🔍💡 Light Sources & Objects Detector", font=('Segoe UI', 18, 'bold'), 
                 text_color=COLORS['primary'], justification='center', expand_x=True, pad=(0, 20))],
        [sg.Frame('Configuration', [
            [sg.Text("Object Masking Distance [cm]:", font=('Segoe UI', 12), text_color=COLORS['text_primary']),
             sg.Push(),
             sg.InputText(key="-DISTANCE-", size=(15, 1), font=('Segoe UI', 12), 
                         border_width=2, pad=(10, 0), justification='center')],
            [sg.Text("💡 Note: Light masking range is fixed at 0.5 meter", 
                     font=('Segoe UI', 10, 'italic'), text_color=COLORS['text_secondary'], 
                     justification='center', expand_x=True, pad=(0, 10))]
        ], font=('Segoe UI', 12, 'bold'), title_color=COLORS['secondary'], 
           border_width=2, relief='solid', pad=(20, 15))],
        [sg.VPush()],
        [sg.Button("🚀 Start Combined Scan", key="-LIGHT-OBJECT_DETECT-", size=(25, 2), 
                   font=('Segoe UI', 12, 'bold'), button_color=(COLORS['surface'], COLORS['warning']),
                   border_width=0, pad=(10, 10)),
         sg.Push(),
         sg.Button("← Back", key="-BACK-", size=(12, 2), 
                   font=('Segoe UI', 12), button_color=(COLORS['surface'], COLORS['text_secondary']),
                   border_width=0, pad=(10, 10))],
        [sg.VPush()],
        [sg.Frame('Scan Results', [
            [sg.Output(key="-OUTPUT-", size=(85, 12), font=('Consolas', 10), 
                      text_color=COLORS['text_primary'], background_color=COLORS['surface'])]
        ], font=('Segoe UI', 12, 'bold'), title_color=COLORS['secondary'], 
           border_width=2, relief='solid', pad=(20, 15), expand_x=True)]
    ]

    window = sg.Window("Light Sources and Objects Detector System", layout, size=(950, 700),
                       resizable=True, return_keyboard_events=True, finalize=True,
                       element_justification='center', margins=(30, 30))
    window.bind("<Escape>", "-ESCAPE-")

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "-BACK-", "-ESCAPE-"):
            send_command('0')
            break
        elif event == "-LIGHT-OBJECT_DETECT-" or event == '\r':
            window["-LIGHT-OBJECT_DETECT-"].update(disabled=True)
            window["-BACK-"].update(disabled=True)
            distance_arr = []
            light_arr = []
            masking_distance_objects = values["-DISTANCE-"]
            masking_distance_lights = 50
            send_command('X')

            angle1 = int(receive_data())
            angle2 = int(receive_data())
            counter = 0
            flag = 0
            while True:
                window.refresh()
                distance = int(receive_data())
                if distance == 9999:
                    break
                arr = measure_two_ldr_samples()
                if counter > 4:  # Servo stuck around first 12 samples
                    light_distance = arr[0] + 1
                    ldr_val1 = arr[1]
                    ldr_val2 = arr[2]

                    if distance > int(masking_distance_objects):
                        window['-OUTPUT-'].update(f"Measured Distance: {distance} [cm]", append=True)
                        window['-OUTPUT-'].Widget.tag_configure("red_text", foreground="red")
                        window['-OUTPUT-'].Widget.insert("end", " (MASKED) ", "red_text")
                        distance_arr.append(0)
                    else:
                        window['-OUTPUT-'].update(f"Measured Distance: {distance} [cm]", append=True)
                        distance_arr.append(distance)

                    window['-OUTPUT-'].update(f" | Estimate Light Distance: {light_distance} [cm]", append=True)

                    if abs(ldr_val1 - ldr_val2) < object_light_epsilon and ldr_val1 < 3 and ldr_val2 < 3:
                        window['-OUTPUT-'].Widget.tag_configure("green_text", foreground="green")
                        window['-OUTPUT-'].Widget.insert("end", " - LIGHT DETECTED", "green_text")
                        if light_distance > int(masking_distance_lights):
                            light_arr.append(0)
                            flag = 0
                            window['-OUTPUT-'].Widget.tag_configure("red_text", foreground="red")
                            window['-OUTPUT-'].Widget.insert("end", " (MASKED) \n", "red_text")
                        else:
                            if flag == 1:
                                light_arr.append(light_distance)
                            else:
                                light_arr.append(0)
                            window['-OUTPUT-'].update("\n", append=True)
                            flag = 1
                    else:
                        window['-OUTPUT-'].Widget.tag_configure("red_text", foreground="red")
                        window['-OUTPUT-'].Widget.insert("end", " (NOISE) \n", "red_text")
                        flag = 0
                        light_arr.append(0)

                counter += 1

            degree_arr = [round(float(5) + i * (float(180) - float(0)) / (len(distance_arr) - 1), 1)
                          for i in range(len(distance_arr))]

            window['-OUTPUT-'].update(f"Distance array: {distance_arr}\n", append=True)
            window['-OUTPUT-'].update(f"Lights array: {light_arr}\n", append=True)
            window['-OUTPUT-'].update(f"Degree array: {degree_arr}\n", append=True)

            draw_scanner_map_lights(distance_arr, light_arr, degree_arr)
            window["-LIGHT-OBJECT_DETECT-"].update(disabled=False)
            window["-BACK-"].update(disabled=False)

    window.close()

def send_file_with_flag(command_char, file_path, is_text_file):
    """Send file with type flag to MSP"""
    send_command(command_char) # sending A
    script = open(file_path)
    print(f"{os.path.basename(script.name)} ({'Text' if is_text_file else 'Script'})") 
    
    if is_text_file: # after this script_flag = 2 
        string = script.read()
        command = len(string)
        send_command_txt((command)) # sending length
        send_command('t')  # send t for Text
         
    else:
        string = command_encoder(script.read())
        command = (len(string))
        send_command_txt((command)) # sending length
        send_command('s')  # s for Script
    send_data(string) # sending data
    receive_ack()

def script_mode():
    global ACK
    global window
    working_directory = "C:\\Users\\97254\\Desktop\\code\\python_vs\\Scripts"

    # Create script slot grid
    script_slots = []
    for i in range(1, 11):
        if i <= 5:  # First row (scripts 1-5)
            if i == 1:
                script_slots.append([])
            script_slots[0].extend([
                sg.Column([
                    [sg.Text(f"Script {i}", font=('Segoe UI', 10, 'bold'), 
                            text_color=COLORS['text_primary'], justification='center')],
                    [sg.Button(f"📤 Upload", key=f"-UPLOAD{i}-", size=(12, 1), 
                              font=('Segoe UI', 9), button_color=(COLORS['surface'], COLORS['accent']),
                              border_width=0)],
                    [sg.Button(f"▶️ Play", key=f"-PLAY{i}-", size=(12, 1), 
                              font=('Segoe UI', 9), button_color=(COLORS['surface'], COLORS['success']),
                              border_width=0)]
                ], element_justification='center', pad=(10, 5))
            ])
        else:  # Second row (scripts 6-10)
            if i == 6:
                script_slots.append([])
            script_slots[1].extend([
                sg.Column([
                    [sg.Text(f"Script {i}", font=('Segoe UI', 10, 'bold'), 
                            text_color=COLORS['text_primary'], justification='center')],
                    [sg.Button(f"📤 Upload", key=f"-UPLOAD{i}-", size=(12, 1), 
                              font=('Segoe UI', 9), button_color=(COLORS['surface'], COLORS['accent']),
                              border_width=0)],
                    [sg.Button(f"▶️ Play", key=f"-PLAY{i}-", size=(12, 1), 
                              font=('Segoe UI', 9), button_color=(COLORS['surface'], COLORS['success']),
                              border_width=0)]
                ], element_justification='center', pad=(10, 5))
            ])

    layout = [
        [sg.Text("📜 Script Management System", font=('Segoe UI', 18, 'bold'), 
                 text_color=COLORS['primary'], justification='center', expand_x=True, pad=(0, 20))],
        [sg.Frame('File Configuration', [
            [sg.Radio("📜 Script File", "RADIO1", key="-SCRIPT-", default=True, 
                     font=('Segoe UI', 11), text_color=COLORS['text_primary']),
             sg.Radio("📄 Text File", "RADIO1", key="-TEXT-", 
                     font=('Segoe UI', 11), text_color=COLORS['text_primary'])],
            [sg.Text("Choose a TXT file to upload:", font=('Segoe UI', 11), 
                     text_color=COLORS['text_primary'])],
            [sg.InputText(key="-FILE_PATH-", size=(60, 1), font=('Segoe UI', 11)),
             sg.FileBrowse("Browse", initial_folder=working_directory, 
                          file_types=[("text Files", "*.txt")], 
                          button_color=(COLORS['surface'], COLORS['secondary']),
                          font=('Segoe UI', 11), border_width=0, size=(10, 1))]
        ], font=('Segoe UI', 12, 'bold'), title_color=COLORS['secondary'], 
           border_width=2, relief='solid', pad=(20, 15))],
        [sg.VPush()],
        [sg.Frame('Script Slots', script_slots, 
                 font=('Segoe UI', 12, 'bold'), title_color=COLORS['secondary'], 
                 border_width=2, relief='solid', pad=(20, 15), element_justification='center')],
        [sg.VPush()],
        [sg.Button("← Back", key="-BACK-", size=(15, 2), 
                   font=('Segoe UI', 12), button_color=(COLORS['surface'], COLORS['text_secondary']),
                   border_width=0, pad=(10, 10))],
        [sg.Frame('Status & Logs', [
            [sg.Text('Ready', key='Script Transferred', font=('Segoe UI', 12, 'bold'), 
                     text_color=COLORS['success'], justification='center', expand_x=True, pad=(0, 10))],
            [sg.Output(key="-OUTPUT-", size=(90, 8), font=('Consolas', 10), 
                      text_color=COLORS['text_primary'], background_color=COLORS['surface'])]
        ], font=('Segoe UI', 12, 'bold'), title_color=COLORS['secondary'], 
           border_width=2, relief='solid', pad=(20, 15), expand_x=True)]
    ]

    window = sg.Window("Script Management System", layout, size=(1000, 800), resizable=True,
                       return_keyboard_events=True, finalize=True,
                       element_justification='center', margins=(30, 30))
    window.bind("<Escape>", "-ESCAPE-")

    while True:
        window.refresh()
        ACK = '0'
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit', "-ESCAPE-"):
            send_command('0')
            break
        elif event in ["-UPLOAD1-", "-UPLOAD2-", "-UPLOAD3-", "-UPLOAD4-", "-UPLOAD5-", "-UPLOAD6-", "-UPLOAD7-", "-UPLOAD8-", "-UPLOAD9-", "-UPLOAD10-"]:
            window["-FILE_PATH-"].update(disabled=True)
            window["-UPLOAD1-"].update(disabled=True)
            window["-UPLOAD2-"].update(disabled=True)
            window["-UPLOAD3-"].update(disabled=True)
            window["-UPLOAD4-"].update(disabled=True)
            window["-UPLOAD5-"].update(disabled=True)
            window["-UPLOAD6-"].update(disabled=True)
            window["-UPLOAD7-"].update(disabled=True)
            window["-UPLOAD8-"].update(disabled=True)
            window["-UPLOAD9-"].update(disabled=True)
            window["-UPLOAD10-"].update(disabled=True)
            window["-PLAY1-"].update(disabled=True)
            window["-PLAY2-"].update(disabled=True)
            window["-PLAY3-"].update(disabled=True)
            window["-PLAY4-"].update(disabled=True)
            window["-PLAY5-"].update(disabled=True)
            window["-PLAY6-"].update(disabled=True)
            window["-PLAY7-"].update(disabled=True)
            window["-PLAY8-"].update(disabled=True)
            window["-PLAY9-"].update(disabled=True)
            window["-PLAY10-"].update(disabled=True)
            window["-BACK-"].update(disabled=True)
            if event == "-UPLOAD1-":
                is_text_file = values["-TEXT-"]
                file_address = values["-FILE_PATH-"]
                send_file_with_flag('A', file_address, is_text_file)
            elif event == "-UPLOAD2-":
                is_text_file = values["-TEXT-"]
                file_address = values["-FILE_PATH-"]
                send_file_with_flag('B', file_address, is_text_file)
            elif event == "-UPLOAD3-":
                is_text_file = values["-TEXT-"]
                file_address = values["-FILE_PATH-"]
                send_file_with_flag('C', file_address, is_text_file)
            elif event == "-UPLOAD4-":
                is_text_file = values["-TEXT-"]
                file_address = values["-FILE_PATH-"]
                send_file_with_flag('D', file_address, is_text_file)
            elif event == "-UPLOAD5-":
                is_text_file = values["-TEXT-"]
                file_address = values["-FILE_PATH-"]
                send_file_with_flag('E', file_address, is_text_file)
            elif event == "-UPLOAD6-":
                is_text_file = values["-TEXT-"]
                file_address = values["-FILE_PATH-"]
                send_file_with_flag('F', file_address, is_text_file)
            elif event == "-UPLOAD7-":
                is_text_file = values["-TEXT-"]
                file_address = values["-FILE_PATH-"]
                send_file_with_flag('G', file_address, is_text_file)
            elif event == "-UPLOAD8-":
                is_text_file = values["-TEXT-"]
                file_address = values["-FILE_PATH-"]
                send_file_with_flag('H', file_address, is_text_file)
            elif event == "-UPLOAD9-":
                is_text_file = values["-TEXT-"]
                file_address = values["-FILE_PATH-"]
                send_file_with_flag('I', file_address, is_text_file)
            elif event == "-UPLOAD10-":
                is_text_file = values["-TEXT-"]
                file_address = values["-FILE_PATH-"]
                send_file_with_flag('J', file_address, is_text_file)
        elif event in ["-PLAY1-", "-PLAY2-", "-PLAY3-", "-PLAY4-", "-PLAY5-", "-PLAY6-", "-PLAY7-", "-PLAY8-", "-PLAY9-", "-PLAY10-"]:
            window["-FILE_PATH-"].update(disabled=True)
            window["-UPLOAD1-"].update(disabled=True)
            window["-UPLOAD2-"].update(disabled=True)
            window["-UPLOAD3-"].update(disabled=True)
            window["-UPLOAD4-"].update(disabled=True)
            window["-UPLOAD5-"].update(disabled=True)
            window["-UPLOAD6-"].update(disabled=True)
            window["-UPLOAD7-"].update(disabled=True)
            window["-UPLOAD8-"].update(disabled=True)
            window["-UPLOAD9-"].update(disabled=True)
            window["-UPLOAD10-"].update(disabled=True)
            window["-PLAY1-"].update(disabled=True)
            window["-PLAY2-"].update(disabled=True)
            window["-PLAY3-"].update(disabled=True)
            window["-PLAY4-"].update(disabled=True)
            window["-PLAY5-"].update(disabled=True)
            window["-PLAY6-"].update(disabled=True)
            window["-PLAY7-"].update(disabled=True)
            window["-PLAY8-"].update(disabled=True)
            window["-PLAY9-"].update(disabled=True)
            window["-PLAY10-"].update(disabled=True)
            window["-BACK-"].update(disabled=True)

            if event == "-PLAY1-":
                send_command('a')
                window['Script Transferred'].update("Playing Script1, Please wait.")
            elif event == "-PLAY2-":
                send_command('b')
                window['Script Transferred'].update("Playing Script2, Please wait.")
            elif event == "-PLAY3-":
                send_command('c')
                window['Script Transferred'].update("Playing Script3, Please wait.")
            elif event == "-PLAY4-":
                send_command('d')
                window['Script Transferred'].update("Playing Script4, Please wait.")
            elif event == "-PLAY5-":
                send_command('e')
                window['Script Transferred'].update("Playing Script5, Please wait.")
            elif event == "-PLAY6-":
                send_command('f')
                window['Script Transferred'].update("Playing Script6, Please wait.")
            elif event == "-PLAY7-":
                send_command('g')
                window['Script Transferred'].update("Playing Script7, Please wait.")
            elif event == "-PLAY8-":
                send_command('h')
                window['Script Transferred'].update("Playing Script8, Please wait.")
            elif event == "-PLAY9-":
                send_command('j')
                window['Script Transferred'].update("Playing Script9, Please wait.")
            elif event == "-PLAY10-":
                send_command('i')
                window['Script Transferred'].update("Playing Script10, Please wait.")

            # while finish_script_flag == 0:
            while True:
                window.refresh()
                opcode = receive_char()
                opcode_dict = {
                    '1': "Increment char on LCD from 0 to 'x'",
                    '2': "Decrement char on LCD from 'x' to 0",
                    '3': "Right rotating char 'x' on LCD Screen",
                    '4': "Setting delay value",
                    '5': "Clearing LCD screen",
                    '6': "Moving sensor to specific angle and measure distance",
                    '7': "Scanning environment from angle1 to angle2",
                    '8': "MSP goes back to sleep mode"
                }

                window['-OUTPUT-'].Widget.tag_configure("blue_text", foreground="blue")
                window['-OUTPUT-'].Widget.insert("end", f"Playing Opcode {opcode}: ", "blue_text")
                print(f"({opcode_dict[opcode]})")

                # print(f"Playing Opcode: {opcode} ({opcode_dict[opcode]})")
                if opcode == '6':
                    window.refresh()
                    distance = int(receive_data())
                    angle = int(receive_data())
                    print(f"Measured Distance: {distance} [cm], Measured Angle: {angle} [°]")

                elif opcode == '7':
                    distance_arr = []
                    angle1 = int(receive_data())
                    angle2 = int(receive_data())

                    while True:
                        window.refresh()
                        distance = int(receive_data())
                        if distance == 999:
                            break
                        print(f"Measured Distance: {distance} [cm]")
                        distance_arr.append(distance)

                    degree_arr = [
                        round(float(angle1) + i * (float(angle2) - float(angle1)) / (len(distance_arr) - 1), 1)
                        for i in range(len(distance_arr))]
                    res = calc_width(distance_arr,10,400)
                     
                    width_arr = [0] * len(distance_arr)
                    pos_arr = []
                    for pair in res:
                        start_angle = pair[0]
                        d_phi = pair[-1] 
                        center_ratio = get_distance_ratio(distance)
                        d_phi_norm = d_phi * center_ratio  # correction factor
                        width_arr[start_angle] = distance_arr[start_angle] * math.sin(math.radians(d_phi_norm))
                        pos_arr.append((distance_arr[start_angle],start_angle + d_phi//2,width_arr[start_angle]))

                    print(f"Distance array: {distance_arr}")
                    print(f"Degree array: {degree_arr}")
                    print(f"Objects: {pos_arr}")
                    draw_scanner_map(pos_arr)

                elif opcode == '8':
                    break

        if ACK == '1':
            file_type = "Text" if values["-TEXT-"] else "Script"
            window['Script Transferred'].update(f"Script1 Transferred ({file_type})")
        elif ACK == '2':
            file_type = "Text" if values["-TEXT-"] else "Script"
            window['Script Transferred'].update(f"Script2 Transferred ({file_type})")
        elif ACK == '3':
            file_type = "Text" if values["-TEXT-"] else "Script"
            window['Script Transferred'].update(f"Script3 Transferred ({file_type})")
        elif ACK == '4':
            file_type = "Text" if values["-TEXT-"] else "Script"
            window['Script Transferred'].update(f"Script4 Transferred ({file_type})")
        elif ACK == '5':
            file_type = "Text" if values["-TEXT-"] else "Script"
            window['Script Transferred'].update(f"Script5 Transferred ({file_type})")
        elif ACK == '6':
            file_type = "Text" if values["-TEXT-"] else "Script"
            window['Script Transferred'].update(f"Script6 Transferred ({file_type})")
        elif ACK == '7':
            file_type = "Text" if values["-TEXT-"] else "Script"
            window['Script Transferred'].update(f"Script7 Transferred ({file_type})")
        elif ACK == '8':
            file_type = "Text" if values["-TEXT-"] else "Script"
            window['Script Transferred'].update(f"Script8 Transferred ({file_type})")
        elif ACK == '9':
            file_type = "Text" if values["-TEXT-"] else "Script"
            window['Script Transferred'].update(f"Script9 Transferred ({file_type})")
        elif ACK == '10':
            file_type = "Text" if values["-TEXT-"] else "Script"
            window['Script Transferred'].update(f"Script10 Transferred ({file_type})")
        else:
            window['Script Transferred'].update("")
        window["-FILE_PATH-"].update(disabled=False)
        window["-UPLOAD1-"].update(disabled=False)
        window["-UPLOAD2-"].update(disabled=False)
        window["-UPLOAD3-"].update(disabled=False)
        window["-UPLOAD4-"].update(disabled=False)
        window["-UPLOAD5-"].update(disabled=False)
        window["-UPLOAD6-"].update(disabled=False)
        window["-UPLOAD7-"].update(disabled=False)
        window["-UPLOAD8-"].update(disabled=False)
        window["-UPLOAD9-"].update(disabled=False)
        window["-UPLOAD10-"].update(disabled=False)
        window["-PLAY1-"].update(disabled=False)
        window["-PLAY2-"].update(disabled=False)
        window["-PLAY3-"].update(disabled=False)
        window["-PLAY4-"].update(disabled=False)
        window["-PLAY5-"].update(disabled=False)
        window["-PLAY6-"].update(disabled=False)
        window["-PLAY7-"].update(disabled=False)
        window["-PLAY8-"].update(disabled=False)
        window["-PLAY9-"].update(disabled=False)
        window["-PLAY10-"].update(disabled=False)
        window["-BACK-"].update(disabled=False)

    window.close()

def send_angle(angle):
    send_data(str(angle).rjust(3, '0'))


def init_uart():
    global s, inChar
    s = ser.Serial('COM7', baudrate=9600, bytesize=ser.EIGHTBITS,
                   parity=ser.PARITY_NONE, stopbits=ser.STOPBITS_ONE,
                   #write_timeout=1,
                   timeout=1)  # timeout of 1 sec so that the read and write operations are blocking,
    # after the timeout the program continues
    # clear buffers
    s.reset_input_buffer()
    s.reset_output_buffer()
    inChar = '0'


def send_data(data_str):
    global s
    for char in data_str:
        a = len(data_str)
        send_command(char)
    time.sleep(0.1)
    s.write(bytes('$', 'ascii'))


def send_command(char):
    global s
    s.write(bytes(char, 'ascii'))
    time.sleep(0.05)  # delay for accurate read/write operations on both ends

def send_command_txt(char):
    global s
    data = char.to_bytes(2, byteorder = 'big')  # b'\x03\x6A'
    first_byte = bytes([data[0]])   # b'\x03'
    second_byte = bytes([data[1]])  # b'\x6A'
    s.write(first_byte)
    time.sleep(0.05)
    s.write(second_byte)
    time.sleep(0.05)


def command_encoder(data_str):
    translated_string = ""
    lines = data_str.split('\n')
    for line in lines:
        line = line.strip()
        if line:
            parts = line.split(' ', 1)
            command = parts[0]
            args = parts[1] if len(parts) > 1 else ""
            hex_value = command_dict.get(command)
            if hex_value is not None:
                opcode = hex(hex_value)[2:].zfill(2)  # Get the opcode in hex format
                hex_args = ''
                if args:
                    # Split the arguments by comma and convert each argument to hex format
                    hex_args_list = [hex(int(arg))[2:].zfill(2).upper() for arg in args.split(',')]
                    hex_args = ''.join(hex_args_list)  # Concatenate the hex arguments
                translated_string += opcode + hex_args + '\n'
    return translated_string


def receive_ack():
    global s, ACK
    #time.sleep(0.25)
    while ACK == '0' or ACK == '':  # delay for accurate read/write operations on both ends
        try:          
            ACK = s.read_until(terminator=b'\0').decode('ascii')
        except TypeError:
            # Fallback for older pySerial versions
            ACK = s.read_until(b'\0').decode('ascii')

def receive_data():
    chr = b''
    while chr[-1:] != b'\n':
        chr += s.read(1)

    return chr.decode('ascii')


def receive_data2():
    chr = b''
    while chr[-1:] != b'\n':
        chr += s.read(1)
    print(chr)
    return chr


def receive_char():
    data = b''
    time.sleep(0.25)  # delay for accurate read/write operations on both ends
    while len(data.decode('ascii')) == 0:
        try:
            data = s.read_until(terminator=b'\n')
        except TypeError:
            
            data = s.read_until(b'\n')
    return data.decode('ascii')


def receive_calib():
    data = b''
    time.sleep(0.25)  # delay for accurate read/write operations on both ends
    while len(data.decode('ascii')) == 0:
        try:
            data = s.read_until(terminator=b'\n')
        except TypeError:
            
            data = s.read_until(b'\n')
    return data


def save_calibration_values(calibration_values):
    with open('calibration_values.txt', 'w') as file:
        for value in calibration_values:
            file.write(str(value) + '\n')

#TODO change the numpay array to just [0] *new length and return array .
def expand_calibration_array(calibration_array, new_length): # linear interpolation 
    expanded_array = np.zeros(new_length) 
    #expanded_array = [0]*len(new_length)
    for i in range(new_length):
        offset = i // 5
        step = i % 5
        if i < 45:
            value = calibration_array[offset] + (calibration_array[offset + 1] - calibration_array[offset]) * step / 5 
        else:
            value = calibration_array[9]
        expanded_array[i] = value

    return expanded_array.tolist()
    #return expanded_array

def measure_two_ldr_samples():
    LDR1_val = int(receive_data()) / 292
    time.sleep(0.25)  # delay for accurate read/write operations on both ends
    if LDR1_val > 1023 / 292:
        return [-1, 0, 0]
    LDR2_val = int(receive_data()) / 292
    fitting_index = find_fitting_index(LDR1_val, LDR2_val)
    return [fitting_index, LDR1_val, LDR2_val]


def find_fitting_index(ldr1_value, ldr2_value): # Binary search for finding the right index to suggest the distance
    # Load calibration values from file
    with open('calibration_values.txt', 'r') as file:
        calibration_arr = [float(line.strip()) for line in file]

    # Calculate average LDR value
    average_ldr_value = (ldr1_value + ldr2_value) / 2

    # Perform binary search on calibration array
    left = 0
    right = len(calibration_arr) - 1
    fitting_value = None

    while left <= right:
        mid = (left + right) // 2
        if calibration_arr[mid] == average_ldr_value:
            fitting_value = calibration_arr[mid]
            break
        elif calibration_arr[mid] > average_ldr_value:
            fitting_value = calibration_arr[mid]
            left = mid + 1
        else:
            fitting_value = calibration_arr[mid]
            right = mid - 1

    # Handle edge cases if the average LDR value is outside the range of the calibration values
    if fitting_value is None:
        if average_ldr_value < calibration_arr[-1]:
            fitting_value = calibration_arr[-1]
        elif average_ldr_value > calibration_arr[0]:
            fitting_value = calibration_arr[0]

    return 49 - calibration_arr.index(fitting_value)


def draw_scanner_map_lights(distances, lights, angles):
    # Define the layout of the PySimpleGUI window
    layout = [
        [sg.Canvas(key="-CANVAS-", size=(800, 800))]
    ]

    # Create the PySimpleGUI window
    window = sg.Window("Scanner Map", layout, finalize=True, resizable=True)

    # Calculate the center point
    center = (0, 0)

    # Create the figure and axis
    fig = plt.figure(figsize=(8, 8))  # Adjust the figsize for a larger plot
    ax = fig.add_subplot(111, polar=True)

    max_distance = max(distances)
    if max_distance == 0:
        max_distance = 50

    # Draw the radar lines with varying colors based on distance
    i = 0
    j = 0
    for distance, light, angle in zip(distances, lights, angles):
        # Convert the angle to radians
        rad_angle = math.radians(angle)

        # Determine the color based on distance
        if light > 0 and distance < 50:
            color = "yellow"
            ax.scatter(rad_angle, distance, color=color, s=50, edgecolors='black', # light insead of distance?
                       label="Light Source" if i == 0 else "")  # remove label?
            i += 1
        else:
            color = "black"
            ax.scatter(rad_angle, distance, color=color, s=10, label="Object" if j == 0 else "")  # remove label?
            j += 1
    plt.legend()  # remove?

    # Set the limits of the plot
    padding = max_distance * 0.1  # Add a 10% padding
    ax.set_ylim(0, max_distance + padding)
    ax.set_yticklabels([])  # Hide radial tick labels
    ax.set_xticklabels([])  # Hide angular tick labels

    radii = ax.get_yticks()
    for radius in radii[1:]:
        ax.text(0, radius, str(radius), ha='center', va='bottom', fontsize=8)

    # Set only the top spine visible
    ax.spines["polar"].set_visible(True)
    ax.spines["polar"].set_color("black")
    ax.spines["polar"].set_linewidth(0.5)
    ax.spines["polar"].set_position(("data", 0))

    # Remove the other spines
    for spine in ax.spines.values():
        if spine.spine_type != "polar":
            spine.set_visible(False)

    # Adjust the y-axis limits to zoom in on the angles
    ax.set_ylim(0, max_distance + padding * 0.3)

    # Modify the angle labels for better visibility
    ax.set_xticks(ax.get_xticks()[::2])
    ax.set_xticklabels([str(int(math.degrees(tick))) + "°" for tick in ax.get_xticks()])

    # Add bold lines for start and end angles
    start_angle = angles[0]-5
    end_angle = angles[-1]-5
    if start_angle != 0:
        ax.plot([math.radians(start_angle), math.radians(start_angle)], [0, max_distance], 'k-', linewidth=3)
        ax.text(math.radians(start_angle), max_distance + padding * 0.15, f"{start_angle}°", ha='center', va='center',
                fontsize=15)
    if end_angle != 180:
        ax.plot([math.radians(end_angle), math.radians(end_angle)], [0, max_distance], 'k-', linewidth=3)
        ax.text(math.radians(end_angle), max_distance + padding * 0.15, f"{end_angle}°", ha='center', va='center',
                fontsize=15)

    # Create the canvas and add it to the PySimpleGUI window
    canvas = FigureCanvasTkAgg(fig, master=window["-CANVAS-"].TKCanvas)
    canvas.draw()
    canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

    window.close()

def draw_scanner_map(pos_arr): 
    
    # Filter objects that meet criteria (width > 3 and distance > 3)
    valid_objects = []
    
    try:
        for i, obj in enumerate(pos_arr):
            if len(obj) >= 3:  # Make sure we have at least 3 elements
                distance, angle, width = obj[0], obj[1], obj[2]
                if width > 1 and distance > 3:
                    valid_objects.append((distance, angle, width))
    except Exception as e:
        sg.popup(f"Error processing pos_arr: {e}")
        return
    
    if not valid_objects:
        sg.popup("No objects found that meet the criteria (width > 3 and distance > 3)")
        return
    
    # Define the layout of the PySimpleGUI window
    layout = [
        [sg.Canvas(key="-CANVAS-", size=(800, 800))],
        [sg.Text(f"Showing {len(valid_objects)} objects with distance > 3 and width > 3", font=('Arial', 12))]
    ]

    # Create the PySimpleGUI window
    window = sg.Window("Scanner Map - Object Detection", layout, finalize=True, resizable=True)

    try:
        # Create the figure and axis
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))

        # Get distances for color mapping
        distances = [obj[0] for obj in valid_objects]
        min_val = min(distances) if distances else 0
        max_val = max(distances) if distances else 1
        
        # Avoid division by zero
        if max_val == min_val:
            max_val = min_val + 1
            
        norm = plt.Normalize(vmin=min_val, vmax=max_val)
        cmap = cm.get_cmap('coolwarm')

        # Plot each valid object
        for distance, angle, width in valid_objects:
            try:
                # Convert angle to radians
                rad_angle = math.radians(angle)
                
                # Get color based on distance
                color = cmap(norm(distance))
                
                # Plot the dot
                ax.scatter(rad_angle, distance, color=color, s=80, alpha=0.8, 
                          edgecolor='black', linewidth=1, zorder=5)
                
                # Add text label above the dot
                label_distance = distance + max_val * 0.1
                label_text = f"D:{distance:.1f}\nA:{angle:.0f}°\nW:{width:.1f}"
                
                ax.text(rad_angle, label_distance, label_text, 
                       ha='center', va='bottom', fontsize=8,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", 
                               alpha=0.8, edgecolor='black'))
                
            except Exception as e:
                print(f"Error plotting object {distance}, {angle}, {width}: {e}")
                continue

        # Set up the plot
        ax.set_ylim(0, max_val * 1.3)  # Give extra space for labels
        ax.set_title("Scanner Map - Detected Objects", fontsize=14, pad=20)
        ax.grid(True, alpha=0.3)
        
        # Add distance circles
        yticks = ax.get_yticks()
        for tick in yticks:
            if tick > 0:
                ax.text(0, tick, f'{tick:.0f}', ha='center', va='bottom', fontsize=8)

        # Attach the matplotlib figure to PySimpleGUI Canvas
        canvas = FigureCanvasTkAgg(fig, master=window["-CANVAS-"].TKCanvas)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

    except Exception as e:
        sg.popup(f"Error creating plot: {e}")
        window.close()
        return

    # Event loop
    while True:
        event, values = window.read(timeout=100)
        if event == sg.WINDOW_CLOSED:
            break
    
    window.close()

def main():
    global s

    # Create modern menu layout with cards
    MenuLayout = [
        [sg.Text("🔬 Advanced Detection & Analysis System", 
                font=('Segoe UI', 24, 'bold'), text_color=COLORS['primary'], 
                justification='center', expand_x=True, pad=(0, 30))],
        [sg.Text("Professional grade proximity detection and environmental scanning", 
                font=('Segoe UI', 12, 'italic'), text_color=COLORS['text_secondary'], 
                justification='center', expand_x=True, pad=(0, 20))],
        [sg.HSeparator(color=COLORS['secondary'], pad=(50, 20))],
        
        # First row of cards
        [sg.VPush()],
        [sg.Button("🎯\nObject Detection\nSystem", key='Object Detector System', 
                  size=(18, 4), font=('Segoe UI', 12, 'bold'), 
                  button_color=(COLORS['surface'], COLORS['primary']),
                  border_width=3, pad=(15, 10)),
         sg.Button("📐\nTelemeter\nMeasurement", key='Telemeter', 
                  size=(18, 4), font=('Segoe UI', 12, 'bold'), 
                  button_color=(COLORS['surface'], COLORS['secondary']),
                  border_width=3, pad=(15, 10)),
         sg.Button("💡\nLight Sources\nDetector", key='Light Sources Detector System', 
                  size=(18, 4), font=('Segoe UI', 12, 'bold'), 
                  button_color=(COLORS['surface'], COLORS['warning']),
                  border_width=3, pad=(15, 10))],
        
        # Second row of cards
        [sg.VPush()],
        [sg.Button("🔍💡\nCombined\nDetection", key='Light Sources and Objects Detector System', 
                  size=(18, 4), font=('Segoe UI', 12, 'bold'), 
                  button_color=(COLORS['surface'], COLORS['accent']),
                  border_width=3, pad=(15, 10)),
         sg.Button("📜\nScript\nManagement", key='Script Mode', 
                  size=(18, 4), font=('Segoe UI', 12, 'bold'), 
                  button_color=(COLORS['surface'], COLORS['success']),
                  border_width=3, pad=(15, 10)),
         sg.Button("🚪\nExit\nApplication", key='Exit', 
                  size=(18, 4), font=('Segoe UI', 12, 'bold'), 
                  button_color=(COLORS['surface'], COLORS['danger']),
                  border_width=3, pad=(15, 10))],
        
        [sg.VPush()],
        [sg.HSeparator(color=COLORS['secondary'], pad=(50, 20))],
        [sg.Text("© 2024 Advanced Detection Systems | Professional Engineering Solution", 
                justification='center', font=('Segoe UI', 9), text_color=COLORS['text_secondary'],
                expand_x=True, pad=(0, 15))]
    ]
    
    window = sg.Window("Advanced Detection & Analysis System", MenuLayout, 
                       size=(950, 650), element_justification='center',
                       margins=(40, 30), resizable=True, finalize=True)
    init_uart()
    send_command('Z')
    msp_calib_arr = []
    ldr_val = receive_data2()
    for i in ldr_val:
        msp_calib_arr.append((4 * i)/ 292.0)
    #flash_expanded_LDR_calibrate_arr = expand_calibration_array(msp_calib_arr, 50)
    #save_calibration_values(flash_expanded_LDR_calibrate_arr)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
            send_command('Q')  # quit
            break
        elif event == 'Object Detector System':
            send_command('1')
            objects_detector()
        elif event == 'Telemeter':
            send_command('2')
            telemeter()
        elif event == 'Light Sources Detector System':
            send_command('3')
            lights_detector()
        elif event == 'Light Sources and Objects Detector System':
            send_command('4')
            light_objects_detector()
        elif event == 'Script Mode':
            send_command('5')
            script_mode()
        else:
            print('You entered ', values[0])

    window.close()


if __name__ == '__main__':
    command_dict = {
        "inc_lcd": 0x01,
        "dec_lcd": 0x02,
        "rra_lcd": 0x03,
        "set_delay": 0x04,
        "clear_lcd": 0x05,
        "servo_deg": 0x06,
        "servo_scan": 0x07,
        "sleep": 0x08
    }
    main()

