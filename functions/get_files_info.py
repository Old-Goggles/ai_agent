import os

def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = "." 
    full_path = os.path.join(working_directory, directory)
    
    allowed = os.path.commonpath([os.path.abspath(working_directory), os.path.abspath(full_path)]) == os.path.abspath(working_directory)
    if not allowed:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if os.path.isdir(full_path) == False:
        return f'Error: "{directory}" is not a directory'

    try: 
        contents = os.listdir(full_path)
        formatted_lines = []

        for content in contents:
            item_full_path = os.path.join(full_path, content)
            is_dir_status = os.path.isdir(item_full_path)
            file_size_bytes = os.path.getsize(item_full_path)
            formatted_lines.append(f'- {content}: file_size={file_size_bytes} bytes, is_dir={is_dir_status}')
    
        final_output_string = "\n".join(formatted_lines)
        return final_output_string
    
    except Exception as e:
        return f"Error: {e}"
