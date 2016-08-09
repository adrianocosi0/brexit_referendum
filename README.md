# brexit_referendum
Execute the code in the notebooks (please do so following their order) to run an analysis on the Brexit referendum in London at the borough level, or just observe the results inside the notebooks and figure folders. A django web interface will also be added to let the user select the factors of interest interactively  

# Prerequisites  

Pandas, Numpy, Matplotlib, sql-alchemy, django, PostgreSql, psycopg2

### NoteBooks folder:

1. Data Collection and Management: Extracts/Downloads data from different sources (Financial Times & London Datastore), after cleaning it returns a pandas DataFrame object, which is then saved as a csv file in the current directory
2. Data Analysis: Loads the DataFrame, defines a function that shows and optionally saves to disk, matplotlib.Figure.figure objects. The graphs are Bubble plots, delineating the relation between % Leave vote by Borough and other factors (e.g. political orientation, earning)
3. Data Modelling: Fits a simple OLS model, showing the statistics and some post-modelling analysis (fitted vs actual values)
4. Data Transfer: Transfers the DataFrame to a sql database, which is then utilized in the Brexit django project

### Figures folder:

Shows the plots originating from the code in the Data Analysis notebook

### Brexit (developing):

Interactive web interface that shows the results of the analysis, with the user being able of selecting the variables to be shown in the graphs
