import subprocess
import os
import shlex

class SystemCommands:

    @staticmethod
    def generate_3d_model(output_dir: str, paramset: str, output_format: str, paramset_filepath: str,
                          openscad_model_filepath: str, dry_run: bool = False) -> bool:
        openscad_command = 'openscad -o "{}/3d/{}.{}" -p "{}" -P "{}" "{}"' \
            .format(output_dir, paramset, output_format, paramset_filepath, paramset, openscad_model_filepath)
        if dry_run:
            print(openscad_command)
            return True
        os.makedirs('{}/3d'.format(output_dir), exist_ok=True)
        try:
            proc = subprocess.run(shlex.split(openscad_command), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            proc.check_returncode()
        except Exception as e:
            print('error executing command: {}'.format(e))
            return False
        print('created \"{}/{}.{}\"'.format(output_dir, paramset, output_format))
        return True

    @staticmethod
    def generate_thumbnail(output_dir: str, paramset: str, paramset_filepath: str,
                           openscad_model_filepath: str, dry_run: bool = False) -> bool:
        openscad_command = 'openscad -o "{}/thumbnail/{}.png" -p "{}" -P "{}" --imgsize=192,192 "{}"' \
            .format(output_dir, paramset, paramset_filepath, paramset, openscad_model_filepath)
        if dry_run:
            print(openscad_command)
            return True
        os.makedirs('{}/thumbnail'.format(output_dir), exist_ok=True)
        try:
            proc = subprocess.run(shlex.split(openscad_command), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            proc.check_returncode()
        except Exception as e:
            print('error executing command: {}'.format(e))
            return False
        print('created \"{}/{}.png\"'.format(output_dir, paramset))
        return True

    @staticmethod
    def generate_poster(columns: int, poster_name: str, output_dir, dry_run: bool = False) -> bool:
        command = 'montage -tile {}x0 -geometry +0+0 "{}/thumbnail/*.png" "{}/{}.png"' \
            .format(columns, output_dir, output_dir, poster_name)
        if dry_run:
            print(command)
            return True
        try:
            proc = subprocess.run(shlex.split(command), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            proc.check_returncode()
        except Exception as e:
            print('error executing command: {}'.format(e))
            return False
        print('created \"{}/poster.png\"'.format(output_dir))
        return True
