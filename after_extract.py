from screenshot_separate import run_adb_command
from prompt_finder import picked_boxes
from prompt_gemini_rizzy import responses
import time
from profile_elements import count

def get_to_top():
    for _ in range(3):
        run_adb_command('adb shell input swipe 500 250 500 2500')
    time.sleep(2)

def heart_centers(boxes):   # returns (x, y, #swipes) for each like icon
    box_centers = []
    for box in boxes:
        tt = []
        tt.append((box[0] + box[2])//2)
        tt.append((box[1] + box[3])//2)
        box_centers.append(tt)

    locations_swipes = []  # x, y', number of swipes needed
    for (x,y) in box_centers:
        temp = [x]
        if y <= 2210 and y >= 210:
            temp.append(y + 97)                                                             # 97 is for the top taskbar
        else:
            temp.append(y - (y//2010)*2010 + 97)
        temp.append(y // 2010)
        locations_swipes.append(temp)

    # hard-coded because prompts are detected bottom to top
    locations_swipes = locations_swipes[::-1]
    return locations_swipes

def parse_response(reply):                                                                  # parses (text+emoji) reply to ascii characters for ADB Keyboard
    reply_ord = []
    for c in reply:
        reply_ord.append(str(ord(c)))
    return ','.join(reply_ord)

def send_like(location, reply):                                                             
    for _ in range(location[2]):                                                            # location[2] has the number of full screen swipes to reach the "reply" prompt
        run_adb_command('adb shell input swipe 500 2220 500 210 4000')                      # full screen dimension based
        time.sleep(1)

    ps = "PS. I made a bot and let it take over Hinge for research purposes"

    run_adb_command(f'adb shell input tap {location[0]} {location[1]}')                     # clicking on the like button of the "reply" prompt
    time.sleep(1)
    run_adb_command('adb shell input tap 540 1940')                                         # selecting the type box
    time.sleep(1)   
    run_adb_command('adb shell ime enable com.android.adbkeyboard/.AdbIME')                 # enabling ADB Keyboard
    time.sleep(1)
    run_adb_command('adb shell ime set com.android.adbkeyboard/.AdbIME')                    # setting ADB Keyboard
    time.sleep(1)
    run_adb_command(f"adb shell am broadcast -a ADB_INPUT_CHARS --eia chars '{reply}'")     # typing the selected reply
    time.sleep(2)
    run_adb_command('adb shell input keyevent 66')                                          # keyevent for enter
    run_adb_command(f"adb shell input text '{ps}'")                                         # typing PS.
    time.sleep(2)
    run_adb_command('adb shell input tap 990 2190')                                         # clicking "Done" button
    run_adb_command('adb shell input tap 540 2110')                                         # clicking "Like" button

def skip():
    run_adb_command('adb shell input tap 109 2105')

if __name__ == '__main__':
    get_to_top()
    if count >= 1:
        like_location = heart_centers(picked_boxes)
        responses = responses[::-1]                                                             # reversed because the prompt locations detected were bottom to top sequentially

        chosen_index, longest_reply = max(enumerate(responses), key=lambda pair: len(pair[1]))  # longest reply out of all 3 prompts, and its corresponding index
        parsed_largest_reply = parse_response(longest_reply)                                

        send_like(location= like_location[chosen_index], reply= parsed_largest_reply)
    else:
        time.sleep(2)
        skip()
