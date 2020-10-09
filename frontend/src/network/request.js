import axios from 'axios'
import qs from 'qs';

export default function request(option) {

    return new Promise((resolve, reject) => {
    // 1.创建axios的实例
    const instance = axios.create({
        baseURL: '/api',
        timeout: 60*60*1000,
        withCredentials: true,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cache-Control': 'no-cache'
        },
        transformRequest: [function (data) {


            return qs.stringify(data);
        }],
    });





    // 2.传入对象进行网络请求
    instance(option).then(res => {
        resolve(res)
    }).catch(err => {
        reject(err)
    })
})

// //请求拦截器
// instance.interceptors.request.use(config=>{
//         console.log(config.baseURL);
//         return config;
//     },
//     error=>{
//         console.log(error);
//     });
//
// //回复拦截器
// instance.interceptors.response.use(
//     result=>{
//         console.log(result.data);
//
//         return result;
//     },
//     error=>{
//         console.log(error);
//     });




}
