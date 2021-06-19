### 前言：

由于新装了一条宽带，选择的套餐中包含一张电信卡（A）。基本套餐有每月1G全国流量和100分钟通话。
加上自己本来也有个卡（B），很多业务都是绑定这张卡（B），但是基本没有流量和通话。该卡设置为最低消费。
因为有流量需求，所以又在晚上办了一张流量卡（C），用于平时在外的共享流量。
目前常用设备支持双卡双待，所以将卡（B）和卡（C），装入。但是卡（A）的短信等开始需要的，所以创建了这个项目来作为日常的使用。

### 基本条件：

- Docker runtime
- 移远EC20模块(提前和卖家联系好，电信卡和其他卡的短信网络不一样)

### 功能：

- 接收短信并发送到手机，延时在半分钟之内。
- 通过手机端的APP机器人发送短信。

### 方案：

1.  ```
    # 检查设备的USB地址
    ls /dev/ttyUSB*
    
    # 设置USB 端口绑定，一般插入的USB口不变，这个ID就不会改变
    udevadm info /dev/ttyUSB2 # 假设上一步gammu identify 能识别的端口是ttyUSB2
    通过输出信息找到如下信息：
    DEVLINKS=/dev/serial/by-path/pci-0000:00:1d.7-usb-0:5:1.2-port0
    这个时候就可以直接修改gammu的port 为上面这个地址
    
    通过增加 /etc/udev/rules.d/ec20_persistent-local.rules 文件固定usb端口
    ACTION=="add", KERNELS=="1-2:1.3", SUBSYSTEMS=="usb", ATTRS{bNumEndpoints}=="03", ATTRS{bInterfaceNumber}=="03", SYMLINK+="ec20"
    这时候就可以通过/dev/ec20来访问设备了。
    systemctl --all | grep ec20
    找到设备的名字，添加到gammu-sms的启动依赖里
    
    ```
    
2.  ```
    # 安装并配置gammu-smsd来接收短信
    sudo apt install -y gammu-smsd python-pip
    sudo pip install pika
    # 一般情况下会有如下报错：Neither a valid executable name nor an absolute path: ${CMAKE_INSTALL_FULL_BINDIR}/gammu-smsd
    # 通过这个命令可以解决：
    sudo sed -i 's|${CMAKE_INSTALL_FULL_BINDIR}|/usr/bin|g' /lib/systemd/system/gammu-smsd.service
    
    # 修改/etc/gammu-smsdrc 设置port为上面第二步固定的值
    # 然后重启服务：
    sudo systemctl daemon-reload
    sudo systemctl restart gammu-smsd
    
    # 检查gammu-smsd的状态，不是running状态 就查看日志解决
    sudo systemctl status gammu-smsd
    ```
    
3.  测试能否收到短信并触发后面的事件
    `sudo apt install pip; sudo pip install -r requirements`
    
    ```
    # 通过python脚本将消息发送到rabbitmq的消息队列中
    # app 接收通知
    ```

4. 通过机器人发送短信
    `10001 -> 10001` 发送10001到10001


### 参考链接：

- https://post.smzdm.com/p/a4wme8zx/
- https://docs.gammu.org/faq/general.html#device-name-always-changes-on-linux-how-to-solve-that
- https://wiki.debian.org/udev#persistent-name
- https://docs.gammu.org/project/index.html
- https://docs.aiogram.dev/en/latest/