<?php

//代理ip列表
const PROXY_LIST = ['36.66.213.167:1080', '47.88.195.233:3128', '202.68.254.99:1080', '188.113.138.238:3128', '181.30.11.71:1080', '189.52.165.134:1080', '69.36.65.214:1080', '92.51.77.126:1080', '177.21.1.34:1080', '82.208.95.64:1080', '114.6.34.194:8080', '190.11.225.222:1080', '176.107.242.142:8080', '142.147.117.1:8080', '162.223.88.243:80', '181.211.191.227:8080', '203.160.172.163:8090', '85.242.171.213:8080', '177.87.45.74:8080', '190.120.123.2:1080', '59.37.163.176:1080', '200.56.200.38:3128', '213.136.77.246:80', '191.37.30.1:1080', '27.131.47.132:8080', '58.176.46.248:80', '116.197.134.130:8080', '213.136.89.121:80', '112.214.73.253:80', '91.103.26.186:1080', '177.37.160.198:3128', '36.37.81.130:8080', '113.21.231.81:1080', '187.94.99.194:1080', '200.68.27.100:3128', '80.1.116.80:80', '178.62.124.132:8118', '103.224.29.26:1080', '41.205.231.202:8080', '200.52.85.99:1080', '190.120.123.3:1080', '93.174.55.82:8080', '101.255.62.202:80', '195.144.232.165:1080', '115.124.73.122:80', '1.179.194.41:8080', '154.73.220.137:8080', '114.199.102.174:8080', '181.49.105.68:8080', '47.90.46.132:3128', '138.36.106.18:3128', '185.21.76.37:8080', '103.36.35.106:8080', '41.33.238.168:1080', '1.179.185.249:8080', '1.179.183.93:8080', '182.253.223.140:8080', '202.150.143.170:8080', '160.202.42.10:8080', '197.220.199.5:443', '122.155.222.98:3128', '197.211.45.4:8080', '120.52.72.59:80', '184.20.102.255:1080', '196.15.141.27:8080', '196.11.90.57:8080', '118.97.24.178:8080', '185.21.76.34:8080', '118.189.157.9:3128', '197.210.196.66:8080', '122.52.133.5:8080', '202.68.254.99:1080', '137.135.166.225:8131', '51.254.132.238:80', '93.63.142.144:80', '78.46.8.204:80', '202.142.158.114:8080', '85.185.244.113:1080', '204.29.115.149:8080', '62.122.100.90:8080', '213.177.105.14:1080', '180.178.104.178:1080', '201.57.249.10:8080', '177.21.12.241:1080', '137.135.166.225:8132', '123.49.34.3:8080', '218.191.247.51:80', '177.135.117.165:3128', '187.94.99.197:1080', '113.253.13.205:80', '180.250.207.162:8080', '177.87.8.50:8080', '45.40.143.57:80', '131.108.103.254:1080', '113.11.87.186:8080', '178.238.229.236:80', '160.202.41.58:8080', '46.16.226.10:8080', '181.39.16.106:8080', '80.245.115.61:8080'];

function curl_via_proxy($url,$proxy_ip,$headers = [],$user_agent = 'curl',$method = 'GET')
{
    $arr_ip = explode(':',$proxy_ip);

    $ch = curl_init($url); //创建CURL对象  
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
    curl_setopt($ch, CURLOPT_HEADER, 0); //返回头部  
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); //返回信息  
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 3); //连接超时时间
    curl_setopt($ch, CURLOPT_TIMEOUT, 5); //读取超时时间
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); //对认证证书来源的检查
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false); //从证书中检查SSL加密算法是否存在
/*    curl_setopt($ch, CURLOPT_PROXYAUTH, CURLAUTH_BASIC); //代理认证模式  
    curl_setopt($ch, CURLOPT_PROXY, "{$arr_ip[0]}"); //代理服务器地址
    curl_setopt($ch, CURLOPT_PROXYPORT, "{$arr_ip[1]}"); //代理服务器端口*/
    curl_setopt($ch, CURLOPT_ENCODING, 'gzip');
    curl_setopt($ch, CURLOPT_USERAGENT, $user_agent);

    //添加头部信息
    if(!empty($headers)){
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    }


    $res = curl_exec($ch);
    $curl_errno = curl_errno($ch);
    if ($curl_errno) {
        curl_close($ch);
        return false;
    }
    curl_close($ch);
    return $res;
}
$headers = array(
    'authority:www.amazon.com',
    'upgrade-insecure-requests:1',
    'user-agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3355.4 Safari/537.36',
    'accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding:gzip, deflate, br',
    'accept-language:zh-CN,zh;q=0.9,en;q=0.8',
);
$url = 'https://www.qq.com/video52073275/naughty_elf_jessa_rhodes_takes_santas_fat_cock_in_her_throat_-_firstclasspov';
//$url = 'http://py.com/test.php';
$content = curl_via_proxy($url,PROXY_LIST[array_rand(PROXY_LIST,1)],$headers);//var_dump($content);exit;
$pattern = "/html5player\.setVideoUrlLow\('(.*?)'\)/";
$pattern = "/html5player\.setVideoUrlHigh\('(.*?)'\)/";
preg_match($pattern,$content,$result);var_dump($result);
die;