#APIs document
## 注册
###request
- Method: **POST**
- URL: /auth/register
- Input Parameters: 
    + name
    + passward
    + email
    + mark ("captcha" 使用验证码验证; else 使用邮箱发送验证链接)
- Response:
    + 参数不全:
    ```
        {
            message: "Arguments mismatch.",
            status: "ERROR"
        }
    ```
    + 发送验证码：
    ```
        {
            message: "Send captcha success.",
            status: "OK"
        }
    ```  
    + 发送邮件验证链接
    ````
        {
            message: "Send confirm email success.",
            status: "OK"
        }
    ````
##验证码验证
###request
- Method: POST
- URL: /auth/validate_captcha
- Input Parameters:
    + captcha (验证码)
    + email
- Response:
    + 参数不全:
    ```
        {
            message: "Arguments mismatch.",
            status: "ERROR"
        }
    ```
    + 邮箱已使用：
    ```
        {
            message: "This email has been used.",
            status: "ERROR"
        }
    ```
    + 验证失败:
    ```
        {
            message: "The captcha is not correct.",
            status: "ERROR"
        }
    ```
    + 验证成功:
    ```
        {
            message: "This user has been confirmed.",
            status: "ERROR"
        }
    ```
##登录
###request
- Method: **POST**
- URL: /auth/login
- Input Parameters:
    + email
    + password
- Response
    + 参数不全:
    ```
        {
            message: "Arguments mismatch.",
            status: "ERROR"
        }
    ```
    + 验证失败：
    ```
        {
            message: "Verification failed.",
            status: "ERROR"
        }
    ```
    + 验证成功：
    ```
        {
            message: "Verification success.",
            status: "OK"
        }
    ```
    + 用户不存在：
    ```
        {
            message: "User doesn't exist",
            status: "ERROR"
        }
    ```

##登出
###request
- Method:
- URL: /auth/logout
- Input Parameters:
- Response:
    + 登出成功:
    ```
        {
            message: "Logout success.",
            status: "OK"
        }
    ```
 
##上传文件
调用此API将文件存放在服务器，然后通过websocket发送一个获得此文件的API的URL到指定聊天室
###request
- Method: POST
- URL: /upload
- Input Parameters:
    + file (the file itself)
    + name
    + user_id
    + chatroom_id
- Response:
    + 发送文件成功
    ```
        {
            message: "Send file successfully.",
            status: "OK"
        }
    ```
    + 发送文件失败
    ```
        {
            message: "Send file failed.",
            status: "ERROR"
        }
    ```
    + 储存文件失败 (文件类型不允许，参数不全，http方法错误)
    ```
        {
            message: "Send file failed.",
            status: "ERROR"
        }
    ```
  
##下载文件
###request
- Method: **GET**
- URL: /upload/<filename>
- Input Parameters:
-Response:
    + 文件不存在：
    ```
        {
            message: "File does not exist.",
            status: "ERROR"
        }
    ```
    + HTTP方法错误：
    ```
        {
            message: "Method mismatch.",
            status: "ERROR"
        }
    ```
    

 
    
    
    
    
        