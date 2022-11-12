
### create a new repository on the command line
echo "# COMP-3106" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/guptamihir418/COMP-3106.git
git push -u origin main

### push an existing repository from the command line
git remote add origin https://github.com/guptamihir418/COMP-3106.git
git branch -M main
git push -u origin main