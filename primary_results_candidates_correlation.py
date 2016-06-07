
import pandas as pd
from pandas import Series,DataFrame
import numpy as np
from scipy.stats import linregress

# For Visualization
import matplotlib.pyplot as plt
import seaborn as sns
#for ipython
#%matplotlib osx

#output folder
OutputFolder='CandidateCorrelation/'
# source data
pr=pd.read_csv('SourceData/primary_results.csv')
#pivoting and drop Null values for clean and easy analysis
pr_piv= pr[['fips', 'candidate','fraction_votes']].pivot(index='fips', columns='candidate', values='fraction_votes')
pr_piv.drop(' No Preference', axis=1, inplace=True)
pr_piv.drop(' Uncommitted', axis=1, inplace=True)
pr_piv=pr_piv.dropna()
#multiindex to make data more readable
c=pr[['party','candidate']].drop_duplicates().sort_values(by=['party','candidate'])
c = c.loc[c['candidate'] != ' No Preference']
c = c.loc[c['candidate'] != ' Uncommitted']
t=c[['party', 'candidate']].apply(tuple, axis=1).tolist()
index = pd.MultiIndex.from_tuples(t, names=['Democrat', 'Republican'])

#heatmap visualization
def heatmap(data,file_name):
  fig, ax = plt.subplots()
  heatmap = sns.heatmap(data, cmap=plt.cm.Blues,annot=True, annot_kws={"size": 8})
  # put the major ticks at the middle of each cell
  # want a more natural, table-like display
  ax.xaxis.tick_top()
  # rotate the
  plt.xticks(rotation=90)
  plt.yticks(rotation=0)
  plt.tight_layout()
  fig.savefig(OutputFolder+file_name)

#if pythonw
#plt.show()

#skipy linregress
#Pearson Correlation
rvalue = DataFrame(np.nan,index=index,columns=index)
rvalue.index.names=['Party','Candidate']
rvalue.index.lexsort_depth
rvalue.columns.lexsort_depth
#PValue
pvalue=DataFrame(np.nan,index=index,columns=index)
pvalue.index.names=['Party','Candidate']
pvalue.index.lexsort_depth
pvalue.columns.lexsort_depth
#StdErr
stderr=DataFrame(np.nan,index=index,columns=index)
stderr.index.names=['Party','Candidate']
stderr.index.lexsort_depth
stderr.columns.lexsort_depth
#
for c_X in pr_piv.columns:
  for c_Y in pr_piv.columns:
    R=linregress(pr_piv[[c_X,c_Y]])
    p_X=index.get_loc_level(c_X,1)[1][0]
    p_Y=index.get_loc_level(c_Y,1)[1][0]
    rvalue.set_value((p_Y,c_Y), (p_X,c_X), R.rvalue)
    pvalue.set_value((p_Y,c_Y), (p_X,c_X),R.pvalue)
    stderr.set_value((p_Y,c_Y), (p_X,c_X), R.stderr)


#democrats only
heatmap(rvalue.loc['Democrat']['Democrat'],'dem_rvalue.png')
heatmap(pvalue.loc['Democrat']['Democrat'],'dem_pvalue.png')
heatmap(stderr.loc['Democrat']['Democrat'],'dem_stderr.png')
#republicans only
heatmap(rvalue.loc['Republican']['Republican'],'rep_rvalue.png')
heatmap(pvalue.loc['Republican']['Republican'],'rep_pvalue.png')
heatmap(stderr.loc['Republican']['Republican'],'rep_stderr.png')

#most anticorrelated republicans
RepRvalue_idxmin=rvalue.loc['Republican']['Republican'].idxmin(axis=0)
RepRvalue_minvalue=rvalue.loc['Republican']['Republican'].min(axis=0)

RepRvalue_min=pd.concat([RepRvalue_idxmin, RepRvalue_minvalue], axis=1)
RepRvalue_min.sort_values(by=1, ascending=True,inplace=True)

#seaborn join plot
#Rep most anticorrelated
i=0
j=0
Candidate1=''
Candidate2=''
while j<2:
    if ((Candidate2<>RepRvalue_min.index[i]) &
    (Candidate1<>RepRvalue_min.index[0][i])):
        Candidate1=RepRvalue_min.index[i]
        Candidate2=RepRvalue_min[0][i]
        print Candidate1+' '+Candidate2
        sns_plot = sns.jointplot(Candidate1,Candidate2,pr_piv,kind='scatter')
        sns_plot.savefig(OutputFolder+Candidate1.replace(" ", "")+'_'+Candidate2.replace(" ", "")+'_joinplot.png')
        j+=1
    i+=1

#Dem most anticorrelated
sns_plot = sns.jointplot('Hillary Clinton','Bernie Sanders',pr_piv,kind='scatter')
sns_plot.savefig(OutputFolder+'HillaryClinton_BernieSanders_joinplot.png')


#Primary results assume a choice between Democrats candidates only or
#Republican candidates only
#So comparing Democrats to Republicans based on these results
#does not have a lot of sense
#However let's look on the picture as a whole
heatmap(rvalue,'rvalue.png')
#seabron for a quick correlation plot which is pandas.DataFrame.corr('pearson')
f, ax = plt.subplots(figsize=(15, 15))
sns_plot = sns.corrplot(pr_piv,annot=True, ax=ax)
plt.savefig(OutputFolder+'corrplot.png')
#Let's look now how high is the possibility of the correlation
#between democrat and republican candidates
#we can not trust such results
heatmap(pvalue,'pvalue.png')

#You can take a look at the StdError of the correlation as well
#heatmap(stderr,'stderr.png')




#Hillary Clinton to Republican
sns_plot = sns.jointplot('Hillary Clinton','Donald Trump',pr_piv,kind='scatter')
sns_plot.savefig(OutputFolder+'HillaryClinton_DonaldTrump_joinplot.png')

sns_plot = sns.jointplot('Hillary Clinton','Carly Fiorina',pr_piv,kind='scatter')
sns_plot.savefig(OutputFolder+'HillaryClinton_CarlyFiorina_joinplot.png')

#seaborn pairplot
sns_plot = sns.pairplot(pr_piv)
sns_plot.savefig(OutputFolder+'pairplot.png')
