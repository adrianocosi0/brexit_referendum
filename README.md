# brexit_referendum
Run the code in the notebooks to run an analysis on the Brexit referendum in London at the borough level  

The notebooks need to be ran in order

### NoteBooks folder:

1. Data Collection and Management: Extracts/Downloads data from different sources (Financial Times & London Datastore), after cleaning it returns a pandas DataFrame object, which is then saved as a csv file in the current directory
2. Data Analysis: Loads the DataFrame, defines a function that shows and optionally saves to disk, matplotlib.Figure.figure objects. The graphs are Bubble plots, delineating the relation between % Leave vote by Borough and other factors (e.g. political orientation, earning)
3. Data Modelling: Fits a simple OLS model, showing the statistics and some post-modelling analysis (fitted vs actual values)
4. Data Transfer: Transfers the DataFrame to a sql database, which is then utilized in the Brexit django project

### Figures folder:

Shows the plots originating from the code in the Data Analysis and Data Modelling notebooks
