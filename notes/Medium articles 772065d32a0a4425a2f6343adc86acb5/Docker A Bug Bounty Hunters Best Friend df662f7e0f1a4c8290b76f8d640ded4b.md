# Docker: A Bug Bounty Hunters Best Friend

# Intro

 Recently I’ve seen the question pop-up a lot: Do you use your native operating system for hacking or a VM? The answer might surprise you dear hacker, i use neither. What i use is containers.

# What is docker?

Docker enables you to seperate your applications from your infrastructures. It consists of a daemon that manages several components of the docker ecosystem. This consists of:

- Network componenets
- Containers
- Images
- Data volumes for storage

![Docker%20A%20Bug%20Bounty%20Hunters%20Best%20Friend%20df662f7e0f1a4c8290b76f8d640ded4b/05C5F6F5-4262-4DFD-B4BA-8583D3051CDD.png](Docker%20A%20Bug%20Bounty%20Hunters%20Best%20Friend%20df662f7e0f1a4c8290b76f8d640ded4b/05C5F6F5-4262-4DFD-B4BA-8583D3051CDD.png)

The daemon manage these components via a REST api. We can use a docker client to communicate with the daemon, which does all the heavy lifting for us. Keen eyed readers might notice that this resembles a client-server architecture and they would be right, that’s exactly what docker is trying to implement.

The Docker client and daemon CAN run on the same server but they don’t have to. 

![Docker%20A%20Bug%20Bounty%20Hunters%20Best%20Friend%20df662f7e0f1a4c8290b76f8d640ded4b/603D9F12-65F0-4FFC-A2F7-58AF6B4BDEF0.png](Docker%20A%20Bug%20Bounty%20Hunters%20Best%20Friend%20df662f7e0f1a4c8290b76f8d640ded4b/603D9F12-65F0-4FFC-A2F7-58AF6B4BDEF0.png)

# Docker components

Before we go any further it’s important we go over some terms. These terms are docker specific and will help us understand the architecture and how we can use docker.

## Daemon

The daemon takes input from the docker client. When docker users run a command like docker run, it gets sent from the client to the daemon which carries them out. The daemon does this using the docker API.

A docker daemon can also communicate with other daemons on the same server or on the network.

## Docker Client

This is the primary way that docker users can use to communicate with the daemon. 

The docker client can communicate with more than 1 daemon.

## Docker registery

Linux users and programmers will undoubteably have heard of repositories. For those of you who have not, a repository is a collection of code or applications that we can use to download or upload code or applications to or from. I know i am grossly oversimplifying this but at the risk of making a lot of people angry, i want to make people understand just enough to where they can follow. 

We can basically see the docker registery as a big repository of images (See below). Docker is configured to look in the docker hub by default but you can even run your own registries.

When you use the “docker pull” command or the “docker run” command, the required images are pulled from their respective registery.

“Docker push” will push your image into your configured registry.

## Docker Objects

### Images

An image is a read only template that describes what is required to build up a container (See below). Often images build upon eachother, for example, you may create an image that builds on the ubuntu image with additional customisations such as apache and your application installed and configured. 

You might want to create your own images or use the ones that are available and built by others. If we want to build our own image, all we have to do is create a docker file that contains the steps required to build our image. Each instruction will create a new layer in our image. This allows us to speed up our development because if we make a change to our dockerfile and rebuild our Image, only the layers that have changed need to be rebuilt.

### Container

A container is a runnable instance of an image. This simply means that we can stop, start or restart our containers based on our images using the docker client which will send our commands to the daemon to be executed.

We can connect our containers to one or more networks, storage solutions or even create a new image based on it’s state.

By default, containers are very well isolated as the name suggest from other containers and the host system. This means that by default you can not access files on your host system from within the container and vica versa. You can however control this behaviour and modify it. 

A container is defined by it’s image and any configuration properties you define for it. It is important to know that containers are not persistent, which means that if you make a change and restart your container, that change will be gone.

# Installing docker

This step is as simple as it can get, all you need is root or admin access to your host OS. 

[https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

[https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

![Docker%20A%20Bug%20Bounty%20Hunters%20Best%20Friend%20df662f7e0f1a4c8290b76f8d640ded4b/84591517-86DD-4538-84FA-23E99431FB1F.jpeg](Docker%20A%20Bug%20Bounty%20Hunters%20Best%20Friend%20df662f7e0f1a4c8290b76f8d640ded4b/84591517-86DD-4538-84FA-23E99431FB1F.jpeg)

You need to download the desktop client on the docker website. After installing it, all you need to do is start up the docker desktop client and you are all set. In the background a docker daemon will start and a client which we can interact with.

## Pulling an image and running it

Go to google, look up the tool you want together with docker hub, example “nikto docker hub”. This will bring you to the docker hub page for that application which will usually have a docker pull command. Execute this command to pull the image. To run the image we can use the docker run command which is usually described on the docker hub page.

If you want to mount a volume, you will need the -v parameter which will look like this:

-v /tmp/localpath:/container/path

![Docker%20A%20Bug%20Bounty%20Hunters%20Best%20Friend%20df662f7e0f1a4c8290b76f8d640ded4b/D973DC7A-046A-4223-A315-5B1A3AE06058.jpeg](Docker%20A%20Bug%20Bounty%20Hunters%20Best%20Friend%20df662f7e0f1a4c8290b76f8d640ded4b/D973DC7A-046A-4223-A315-5B1A3AE06058.jpeg)