# AST_parser
Extension program of ANDROGUARD for using its AST data

## When you using this project you have to copy your dataSet(APK or jar) into 'ASTParser/data/'

## How to install this project
1. $ cd [root directory of this project]
2. $ docker build -t ast ./

## How to Use it
1. Move your APK that want you to analyze to [./data] directory
   (in this case, your APK name should not have whitespace (' ') !!)
2. $ docker run -it --rm -v [Directory_that_you_want_to_save_result]:/root/result/ ast