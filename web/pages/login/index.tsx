import React, { useMemo, useState } from 'react';

import { useTranslation } from 'react-i18next';
import styles from '../../styles/login.module.css'
import { apiInterceptors, login } from '@/client/api';
import { TOOKEN_KEY } from '@/utils';
import { useRouter } from 'next/router';

function Login() {
  const [username,setUserName] = useState<string>('');
  const [password,setPassWord] = useState<string>('');
  const { t } = useTranslation();
 const router = useRouter();
  const [loading, setLoading] = useState(false);

  async function loginApp(){
    console.log(username,password)
    let [a,b,c,d] =  await  apiInterceptors(login({username:username,password:password,grant_type:""}))
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
        <div className={styles.login_wrapper}>
          <div className={styles.header}>Login</div>
          <div className="form-wrapper">
            <input type="text" name="username" placeholder="username" className={styles.input_item} value={username} onChange={e =>{setUserName(e.target.value)}}/>
            <input type="password" name="password" placeholder="password" className={styles.input_item} value={password} onChange={event => {setPassWord(event.target.value)}} />
            <div className={styles.btn} onClick={loginApp} >Login</div>
          </div>
          <div className={styles.msg}>
            Don't have account?
            <a className = {styles.a} href="#">Sign up</a>
          </div>
        </div>
      </div>
  );
}

export default Login;
