# RTSP Camera to WebRTC Streaming System (MediaMTX + EC2 + Nginx)

## 📌 Overview

This project streams video from an RTSP camera, pushes it to a MediaMTX server running on AWS EC2, and redistributes it to viewers using WebRTC. Nginx is used as a reverse proxy to serve and secure the web interface for viewers.

---

## 🏗️ System Architecture
RTSP Camera -> Python Streamer (aiortc) -> MediaMTX (RTSP -> WebRTC gateway) ->
EC2 Instance (AWS) -> Nginx Reverse Proxy -> Web Clients (Browser via WebRTC)


---

## 🚀 Features

- RTSP camera ingestion
- WebRTC low-latency streaming
- MediaMTX for stream handling
- AWS EC2 deployment
- Nginx reverse proxy for web access
- Multi-viewer support via browser

---

## 🧰 Tech Stack

- Python (aiortc, aiohttp)
- MediaMTX (RTSP/WebRTC server)
- Nginx
- AWS EC2 (Debian)

---

## ⚙️ Requirements

### Server (EC2)
- Debian 13
- Nginx
- MediaMTX
- Python 3.8+


📦 Installation

1. Clone Repo
git clone https://github.com/maivinhau2601-rgb/Camera-WebRTC.git

2. Install dependencies
Open and run cctv-stream.sh file on the local device 

3. Setup EC2

### VPC setup
To deploy this project on AWS, a basic VPC setup is used to provide networking for the EC2 instance.

#### Steps:
    1. Create a new VPC 
    2. Create a public subnet within the VPC
    3. Attach an Internet Gateway (IGW) to the VPC
    4. Configure a route table to allow internet access (0.0.0.0/0 → IGW)
    5. Enable auto-assign public IP for the subnet
    6. Launch EC2 instance inside the public subnet


### Security Group - Inbound
    Port        Protocol        Source
    8889        TCP             0.0.0.0/0
    8889        UDP             0.0.0.0/0
    8189        UDP             0.0.0.0/0
    443         HTTPs           0.0.0.0/0
    80          HTTP            0.0.0.0/0
    All         All             Your IP


### Elastic IP (Static Public IP Setup)
To ensure the EC2 instance always has a fixed public IP address:

#### Steps:
    1. Go to AWS Console → EC2
    2. Navigate to Network & Security → Elastic IPs
    3. Click Allocate Elastic IP address
    4. Click Allocate
    5. Select the newly created Elastic IP
    6. Click Actions → Associate Elastic IP address
    7. Choose your EC2 instance
    8. Click Associate


### Nginx Installation and Configuration
    1. Follow this link to install: https://nginx.org/en/linux_packages.html#Debian
    2. Then cd /etc/nginx/sites-available/default
    3. After that copy nginx-config.txt and paste it to /etc/nginx/sites-available/default
    4. Finally link that dir to /etc/nginx/sites-enabled/default by 
            ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

    Testing and running nginx:  nginx -t
                                systemctl start nginx

### Frontend and Backend Setup
    1. Put backend.py, login.html and stream.html in /var/www/html
    (Optinal) if you want to run backend.py in the background, you can use systemd service
    2. Then run server-setup.sh by using bash server-setup.sh

4. Domain Setup
You can use cloudflare to buy and manage your domain
Then assign you domain name with your ec2 public ip address

### Troubleshooting
#### Stream not showing
        - Check MediaMTX logs
        - Verify RTSP URL
        - Check firewall ports (8554, 8889, etc.)

#### WebRTC fails
        - Ensure ICE/STUN configuration is correct
        - Check browser console logs
        - Nginx 502 error
        - Backend service not running
        - Wrong proxy_pass address

### Performance Notes
- WebRTC latency: ~200–500ms
- Depends on network + EC2 instance type

### Automation (Jenkins)
Ongoing ....
