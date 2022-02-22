#!/bin/bash

helpFunction()
{
   echo ""
   echo "Usage: $0 -m MODEL_DIR -c CONFIG_FILE -o OUTPUT_DIR"
   echo -e "\t-m Path to model directory"
   echo -e "\t-c Path to config file"
   echo -e "\t-o Path to output directory"
   exit 1 # Exit script after printing help
}

while getopts "p:m:c:o:" opt
do
   case "$opt" in
      m ) MODEL_DIR="$OPTARG" ;;
      c ) CONFIG_FILE="$OPTARG" ;;
      o ) OUTPUT_DIR="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$MODEL_DIR" ] || [ -z "$CONFIG_FILE" ] || [ -z "$OUTPUT_DIR" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

# Begin script in case all parameters are correct
rm -rf $OUTPUT_DIR
xvfb-run -a 3dgen \
  --model-dir "$MODEL_DIR" \
  --conf-file "$CONFIG_FILE" \
  --output-dir "$OUTPUT_DIR" \
  --thumbnails

montage -tile 11x0 -geometry +0+0 "$OUTPUT_DIR/thumbnail/*.png" "$OUTPUT_DIR/poster.png"
