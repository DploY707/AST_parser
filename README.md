# AST_parser
Extension program of ANDROGUARD for using its AST data

## How to install this project
1. $ cd [root directory of this project]
2. $ docker build -t ast ./

## How to Use it
1. Move your APK that want you to analyze to [./data] directory
   (in this case, your APK name should not have whitespace (' ') !!)
2. $ docker run -it --rm ast