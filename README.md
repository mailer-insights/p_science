# Dependencies:

## PDF Scraper
### 1) You will need a Java Runtime in order to scrape a pdf containing teaching hospitals

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

### 2) Setup Virtual Environment
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements
```


<<<<<<< HEAD
### 3) (Optional) Setting up Jupter Notebook to use Virtual Environment Kernel
=======
###3) (Optional) Setting up Jupter Notebook to use Virtual Environment Kernel
#### If you want to see my jupyter notebook and thought process
>>>>>>> b438f7bdc90a094b23362b7c3f5c2e6a0c161eb7

```
python -m ipykernel install --name=analysis
jupyter notebook
```


### 4) Using the class version instead of the notebook

```
python sales.py
```

## Results

Both CSV and interactive plots will appear in the results folder
If running into JVM errors related to the pdf scraper see #1 in the dependency step

# TODO:
- [ ] Find a better teaching hospitals dataset with matching hospital ids
- [ ] Map revenue by Zip on interactive Map
- [ ] To deal with JVM dependency needed for PDF scraper use Docker container
