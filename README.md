# Dependencies:

## PDF Scraper
###1) You will need a Java Runtime in order to scrape a pdf containing teaching hospitals

Install
```
brew cask install java
```

Verify
```
brew cask info java
```

Note:
If on Mac OS Catalina you might run into permissions issues for java
follow these instructions: https://apple.stackexchange.com/questions/372744/cannot-install-jdk-13-01-on-catalina

###2) Setup Virtual Environment
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements
```


###3) (Optional) Setting up Jupter Notebook to use Virtual Environment Kernel

```
python -m ipykernel install --name=analysis
jupyter notebook
```


###4) Using the class version instead of the notebook

```
python sales.py
```
