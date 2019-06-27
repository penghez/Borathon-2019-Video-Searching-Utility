import os
import json

def convert(folder_path, file_path, video_name):
    convert_json = []
    with open(file_path, 'r') as vtt_file:
        line_no = 1
        all_lines = vtt_file.readlines()
        while line_no < len(all_lines):
            try: 
                cur_line = {}
                cur_line['video_name'] = video_name
                
                line_no = trim_blank_lines(all_lines, line_no)
                cur_line['row_id'] = all_lines[line_no].strip('\n')
                
                line_no += 1
                line_no = trim_blank_lines(all_lines, line_no)
                cur_line['start_timestamp'], cur_line['end_timestamp'] = \
                    [x.strip() for x in all_lines[line_no].strip('\n').split('-->')]
                
                line_no += 1
                line_no = trim_blank_lines(all_lines, line_no)
                cur_line['row_content'] = all_lines[line_no].strip('\n')
                print(cur_line)
                convert_json.append(cur_line)
            except:
                pass
            
            line_no += 1

        with open(os.path.join(folder_path, video_name + '.json'), 'w') as json_file:
            for j in convert_json:
                json_file.write(json.dumps(j))
                json_file.write('\n')

def trim_blank_lines(all_lines, line_no):
    while line_no < len(all_lines) and all_lines[line_no].strip() == '':
        line_no += 1
    return line_no

if __name__ == "__main__":
    folder_path = "./Zoom Videos"
    
    for video_folder_name in os.listdir(folder_path):
        video_folder = os.path.join(folder_path, video_folder_name)
        if os.path.isdir(video_folder):
            for file_path in os.listdir(video_folder):
                if file_path.endswith(".vtt"):
                    convert(video_folder, os.path.join(video_folder, file_path), video_folder_name)

