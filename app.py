from flask import Flask, request, redirect, url_for
import os
import fileenc
import shutil
app = Flask(__name__)
#======================================================================
def log(text):
    print(f'LOG : {text}')

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        log("E: Failed to create the directory.")
#=======================================================================

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def auth_token(mode, key):
    global user_session
    if mode == 'r':
        print('read')
        try:
            fileenc.decrypt(authtoken_dir+'.enc', key)
        except:
            log('비밀번호 에러')
            quit()
        with open(authtoken_dir, 'rt') as file:
            data = file.read()
        print(data)
        if data == "PASS":
            user_session = True
            log("logined")
            fileenc.encrypt(authtoken_dir, key)
        else:
            user_session = False
            log('login failed')


    elif mode == 'w':
        print('w')
        #파일 쓰기
        f = open(authtoken_dir, 'w')
        f.write('PASS')
        f.close()
        fileenc.encrypt(authtoken_dir, key)
        log("AUTH TOKEN was generated")


def check_user(auth_key):
    if os.path.isfile(authtoken_dir+'.enc'):
        auth_token('r', auth_key)
    else:
        log('NEW user')
        createDirectory('data')
        auth_token('w', auth_key)
        log("Password SET - Never forget password!")
        log("- 프로그램 재실행 -")
        check_user(auth_key)


def check_files():
    if os.path.isdir(current_dir+'\encrypted'):
        print("encrypted 폴더 존재")
    else:
        log('encrypted 폴더 생성')
        createDirectory('encrypted')

    if os.path.isdir(current_dir+'\decrypted'):
        print("decrypted 폴더 존재")
    else:
        log('decrypted 폴더 생성')
        createDirectory('decrypted')

def login(password):
    global current_dir
    global authtoken_dir
    global user_key
    global user_session


    current_dir = f"{os.getcwd()}"
    authtoken_dir = current_dir+'\data\.authtoken'

    print(f'DIRECTORY : {current_dir}')
    print(f'AUTH_DIRECTORY : {authtoken_dir}')
    user_session = False
    user_key = password

        
    check_user(user_key)
    log(f"login status : {user_session}")

    check_files()
    return user_session

def edit_fuction(mode, key):
    #복호화된, 암호화할 파일 목록임
    enc_file_list = os.listdir(current_dir+'\decrypted')
    #암호화된, 복호화할 파일 목록임
    dec_file_list = os.listdir(current_dir+'\encrypted')
    log(enc_file_list)
    log(dec_file_list)

    if mode == 'enc':
        for file in enc_file_list:
            fileenc.encrypt(current_dir+'\decrypted'+f'\{file}', key)
        #암호화된 파일 목록임!
        enc_file_list = os.listdir(current_dir+'\decrypted')
        for file in enc_file_list:
            shutil.move(current_dir+'\decrypted'+f'\{file}',current_dir+'\encrypted'+f'\{file}')


    if mode == 'dec':
        for file in dec_file_list:
            fileenc.decrypt(current_dir+'\encrypted'+f'\{file}', key)
        #암호화된 파일 목록임!
        dec_file_list = os.listdir(current_dir+'\encrypted')
        for file in dec_file_list:
            shutil.move(current_dir+'\encrypted'+f'\{file}',current_dir+'\decrypted'+f'\{file}')
        
        

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#                SLICg528Gu4m76axR76n_41vnQbbrZyLhAgysR3W2Ko=



@app.route('/')
def index():

    return '''
<form action="/home" method="post">
        <p>비밀번호 : <input type="text" id="input" name="input"></p>
		<p>비밀번호를 입력하고 제출버튼을 누르세요. <input type="submit" value="제출" onclick="alert('제출 완료!')" /></p>
	</form>
'''

@app.route('/home', methods=['POST'])
def home():
    global login_key
    login_key = request.form['input']
    if login(login_key):
        return '''<p>LOGIN SUCCESS</p>
        <form action="/edit" method="post">
        <p>암호화 : <input type="text" id="input" name="input"></p>
		<p>폴더의 파일을 암호화/복호화하시려면 enc/dec를 입력하세요 <input type="submit" value="제출" onclick="alert('제출 완료!')" /></p>
	</form>
        '''

    else:
        return "FAILED"

@app.route('/edit', methods=['POST'])
def edit():
    value = request.form['input']
    if value == 'enc':
        print(login_key)
        edit_fuction('enc', login_key)
        return "암호화 요청됨"
    elif value == 'dec':
        print(login_key)
        edit_fuction('dec', login_key)
        return "복호화 요청됨"



app.run(debug=True)












