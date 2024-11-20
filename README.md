# resume-enhancer

### To upload from localhost

1. Pull .env values from Lambda function on AWS console
2. Create Python Virtual Env within the resume-enhancer directory
   1. python -m venv .venv
   2. source .venv/bin/activate (this should source your local python command to use the venv python version)
   3. pip install -r requirements.txt
3. Run python S3/upload.py
   1. If this doesn't work, then run the file using the VSCode file play button on the top right bar
