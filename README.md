### @Zhengli
![alt text](https://raw.githubusercontent.com/andreasbm/readme/master/assets/logo-shadow.png)

Zhengli---Catalogue and organize your book collection based off images shot from your camera. We are offering an API service
that uses data science to automatically detect and recognize books that it finds in user submitted images of bookshelves. 

Future Features:
Organize books by genre and categories.

## How to use Zhengli
```
git clone https://github.com/dingchaoz/bookshelf.git
docker build -t zhengli .
docker run --rm -p 5000:8080 zhengli 
```
then send a book shelf image to the service
```
curl -X POST -H 'content-type: application/json' --data '{"file":"IMG_20190904_155939359.jpg"}' http://127.0.0.1:5000/api
```
sample information returned about the books from the shelf image
```
ddc is 793.9 and best match book is {'title': 'Warcraft Ii: Beyond The Dark Portal: Official Secrets And Solutions (secrets Of The Games Series)', 'image': 'https://images.isbndb.com/covers/78/71/9780761507871.jpg', 'title_long': 'Warcraft Ii: Beyond The Dark Portal: Official Secrets And Solutions (secrets Of The Games Series)', 'date_published': '1996', 'publisher': 'Prima Games', 'synopsys': 'With This Expansion Disk To Warcraft Ii: Tides Of Darkness, Players Can Extend Their Warcraft Experience As They Delve Into The Orcs Homeland For The First Time To Experience An Entirely New Set Of Challenges. Players Can Compete In Head-to-head Battles Against As Many As Eight Players.', 'authors': ['Mark Walker'], 'isbn13': '9780761507871', 'msrp': '14.99', 'publish_date': '1996', 'binding': 'Paperback', 'isbn': '0761507876'}
```
## Deploy zhengli to EC2
First we need to share the image to Docker hub so you may download it from EC2 instance, there are 3 simple steps:
- ```docker login --username username```
prompts for password if you omit --password which is recommended as it doesn't store it in your command history
then we tag it with your username and repo name
- ```docker tag my-image username/my-repo```
push to docker hub
- ```docker push username/my-repo```
Now that your image is online, anyone who has docker installed can play with your app by typing just a single command.
- Go to EC2 in AWS, configuring inboud ports in security group:
Go to the "Network & Security" -> Security Group settings in the left hand navigation,find the Security Group that your instance is apart of Click on Inbound Rules,u se the drop down and add HTTP (port 80). 
and also choose the right VPC group used in this demo in developer_qa environment.
Follow the next steps to install docker assuing using AWS LINUX AMI:
- Update the installed packages and package cache on your instance.

```
sudo yum update -y
```
- install docker
```
sudo yum -y install docker
```
Start docker service
```
sudo service docker start
```
Verify docker is on
```
sudo docker info
```
If you’re using a different Linux distribution other than Ubuntu, you may need different installation command line.
Once docker is installed, run the following command to start the app.
```
docker run -d -p 80:8080 username/repo
```
Copy paste the public ip address of the EC2 instance, then paste it into the following curl request, for example ec2-174-129-182-222.compute-1.amazonaws.com is the public IP in this case
```
curl -X POST -H 'content-type: application/json' --data '{"file":"IMG_20190904_155939359.jpg"}' ec2-174-129-182-222.compute-1.amazonaws.com:80/api```
- Stop and prune the containers
```
docker stop $(docker ps -a -q)
```

## How does Zhengli work?
At a high level, Zhengli uses a combination of computer vision, image processing, and natural language processing to detect books in images of bookshelves. Breaking it down a little further, these are the main steps involved. A more detailed description of each step in the algorithm is presented in the following sections.

Zhengli's algorithm:

- Detect all instances of book shapes in the image
- Split books into individual one by its spine
- Detect all instances of text in each book image
- Spell correct text detected
- Extract book title, publisher, author from detected text associated with a book
- Perform a search on the book, titile and publisher for a match on open library API
- Validate the book using its original camera image and its image on open library website
- Get the ISBN number from the book
- Get the Deway Decimal number and other
- Return the following information about the books: title, author, publisher, publishing date, ISBN, deway decimal number.

## Authors
Sarah Hudspeth, Dingchao Zhang

## Contributing
Contributions, issues and feature requests are welcome.
Feel free to check issues page if you want to contribute.
Check the contributing guide.
