import React, { useMemo, useState } from 'react';

import { useTranslation } from 'react-i18next';
import styles from '../../styles/login.module.css'
import { apiInterceptors, login } from '@/client/api';
import { TOOKEN_KEY } from '@/utils';
import { useRouter } from 'next/router';
import { notification } from 'antd';

function Login() {
  const [username,setUserName] = useState<string>('');
  const [password,setPassWord] = useState<string>('');
  const { t } = useTranslation();
 const router = useRouter();
  const [loading, setLoading] = useState(false);

  async function loginApp(){
    console.log(username,password)
    let [a,b,c,d] =  await  apiInterceptors(login({username:username,password:password,grant_type:""}))
    if(b==null)return
    debugger
    // @ts-ignore
    let {access_token}  = b
    // @ts-ignore
    let {success,error_code} = c
    if(success === true&& error_code == null){
      localStorage.setItem(TOOKEN_KEY,access_token)
      router.push("/")
    }
  }



  return (
    <div className={styles.container}>

      <video muted  className={styles.video} src='/2.mp4' autoplay="autoPlay" loop = "loop" ></video>

      <div className={styles.login_wrapper}>

        <div className={styles.header}>智能问答平台</div>
        <div className="form-wrapper">
          <input type="text" name="username" placeholder="username" className={styles.input_item} value={username}
                 onChange={e => {
                   setUserName(e.target.value)
                 }} />
          <input type="password" name="password" placeholder="password" className={styles.input_item} value={password}
                 onChange={event => {
                   setPassWord(event.target.value)
                 }} />
          <div className={styles.btn} onClick={loginApp}>登陆</div>
        </div>
        <div className={styles.msg}>
          还没有账号?
          <a className={styles.a} href="#">注册</a>
        </div>
      </div>
    </div>
  );
}

export default Login;
