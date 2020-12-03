# 离线扫玛实现

## 流程图

![1550827152291](images/20190222175607.png)


## android离线生成二维码

- 待加签字符串 user=<用户唯一标识 手机号>&time=<时间戳 秒>
  - 例如：user=18582510916&time=1556159837
- 使用SHA1加签名 (见最后签名方式)
  - 得到签名 sign=bac79d79038209e983c8c158beec8ddc673db34b
  - 拼接
  - user=18582510916&time=1556159837&sign=bac79d79038209e983c8c158beec8ddc673db34b
- 使用RSA私钥加密
  - pv5eVG5lzGojeIW5cyF+MRIGQcBKscFNgwy/Q/0D8HXegPbx523rQD71x+AeDVYi6WispdH0KbNlrHZwgVcbeNCPca4q1OmlNEzPZZrdBY2V38z4JLZieESdBUA7mSDVFcXNqt9VZ7/d+MmCUOwAoaPLoolj7hLgVhnGY+0f4cw=
- 增加二维码协议头 woff://
  - woff://pv5eVG5lzGojeIW5cyF+MRIGQcBKscFNgwy/Q/0D8HXegPbx523rQD71x+AeDVYi6WispdH0KbNlrHZwgVcbeNCPca4q1OmlNEzPZZrdBY2V38z4JLZieESdBUA7mSDVFcXNqt9VZ7/d+MmCUOwAoaPLoolj7hLgVhnGY+0f4cw=
- 生成二维码

## 扫玛设备验证及上传订单数据

**注意下列值均可设置:**user=18582510916&time=1556159837&sign=bac79d79038209e983c8c158beec8ddc673db34b

- 离线RSA公钥
  - rsa_public_key.pem
- 在线RSA公钥
  - rsa_public_key.pem
- 二维码超时时间 5分钟
- 验证二维码使用的盐 
  -  7af61707e48da90f44b87aad508933d6
- 上传订单使用的盐 
  -  7af61707e48da90f44b87aad508933d6
- 订单回调地址 https://wgxing.com/callback/qrcode-callback/

## 验证步骤

- 获取二维码信息  **won为在线** ，**woff为离线** 
  
  - won://pv5eVG5lzGojeIW5cyF+MRIGQcBKscFNgwy/Q/0D8HXegPbx523rQD71x+AeDVYi6WispdH0KbNlrHZwgVcbeNCPca4q1OmlNEzPZZrdBY2V38z4JLZieESdBUA7mSDVFcXNqt9VZ7/d+MmCUOwAoaPLoolj7hLgVhnGY+0f4cw=
  
- 除去协议头

  - pv5eVG5lzGojeIW5cyF+MRIGQcBKscFNgwy/Q/0D8HXegPbx523rQD71x+AeDVYi6WispdH0KbNlrHZwgVcbeNCPca4q1OmlNEzPZZrdBY2V38z4JLZieESdBUA7mSDVFcXNqt9VZ7/d+MmCUOwAoaPLoolj7hLgVhnGY+0f4cw=
  
- RSA公钥解密得到
    - user=18582510916&time=1556159837&sign=bac79d79038209e983c8c158beec8ddc673db34b

- 验证签名(见最后签名方式) 和 时间戳
  - 对比sign 和sign2是否相同，不相同验证不成功
  - 验证时间戳是否在规定设置时间内，超出验证不成功


## 上传订单信息

```python
{
	"mobile": "18508217500",    # 匹配成功的手机号
    "up_stamp": "1530254789",   # 精确到秒,  上送的时间戳
    "device_no": "",            # 设备UniqueId  
    "sign": "cb520702ff4c0f251ca8d37591237d52ced0ded7",
    "verify_type": 1,           #  1:无感行二维码回调
    "longitude": "经度",	        # 扫码时所处的经纬度
	"latitude": "纬度"
}

# 订单数据使用以下签名方式
```



## 签名方式

- 设所有发送的数据为集合M，将集合M内非空参数值的参数按照参数名ASCII码从小到大排序（字典序），使用URL键值对的格式（即key1=value1&key2=value2…）拼接成字符串stringA
  - 特别注意以下重要规则：
      - 参数名ASCII码从小到大排序（字典序）；
      - 如果参数的值为空不参与签名；
      - 参数名区分大小写；
      - 传送的sign参数不参与签名
- 拼接w_salt, 例如：stringB = stringA&w_salt=(提供给你的 salt 值)
- 使用 SHA1 算法得到签名：sign=SHA1(stringB)

