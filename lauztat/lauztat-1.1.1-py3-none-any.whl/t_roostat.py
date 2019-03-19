import numpy as np
import matplotlib.pyplot as plt
from skhep.dataset.numpydataset import *
import uproot
from skhep.dataset.selection import Selection
import ROOT
from Utilities.utilities import destruct_objects
from Utilities.RooFit import RooDataset, RemoveEmptyBins
from PyLHCb.Root.RooFitUtils import ResidualPlot
import probfit
import iminuit

# Proxies for RooFit classes
RooFit        = ROOT.RooFit
RooRealVar    = ROOT.RooRealVar
RooArgList    = ROOT.RooArgList
RooArgSet     = ROOT.RooArgSet
RooDataSet    = ROOT.RooDataSet
RooAddPdf     = ROOT.RooAddPdf
RooProdPdf    = ROOT.RooProdPdf
RooExtendPdf  = ROOT.RooExtendPdf
RooConst      = ROOT.RooFit.RooConst
RooConst      = ROOT.RooFit.RooConst
RooExponential= ROOT.RooExponential
RooStats      = ROOT.RooStats
RooGaussian   = ROOT.RooGaussian
RooWorkspace  = ROOT.RooWorkspace
RooWorkspace.rfimport = getattr(RooWorkspace,'import')


#background only
np.random.seed(10)
tau = -2.0
beta = -1/tau
data = np.random.exponential(beta, 1000)
data = data[(data > 0.1) & (data < 3)]
plt.hist(data, bins=100, histtype='step');


exp_n = probfit.Normalized(probfit.exponential, (0.1,3.))
UL_exp = probfit.UnbinnedLH(exp_n, data)

initial_params = {"lambda":  2.0,  "limit_lambda":    (0.0, 5.0) , "error_lambda"   : 0.05,}

minuit_exp = iminuit.Minuit(UL_exp, **initial_params, pedantic=True)
minuit_exp.migrad();

np.random.seed(0)
tau = -2.0
beta = -1/tau
data = np.random.exponential(beta, 300)
peak = np.random.normal(1.2, 0.1, 10)
data = np.concatenate((data,peak))
data = data[(data > 0.1) & (data < 3)]

plt.hist(data, bins=100, histtype='step');

ws = RooWorkspace("ws")
x = RooRealVar("x","x",0.1,3.0)
ws.rfimport(x)

roodataset = RooDataset( "data", x) 
roodataset.fill( data )
roodataset.Print('v')
roodataset.to_wspace( ws )

### signal
mean = RooConst(1.2)
sigma = RooConst(0.1)
gauss = RooGaussian("signal","signal", x, mean, sigma)
nsig  = RooRealVar("nsig", "nsig", 0, -10, len((data)))
gauss_norm = RooExtendPdf("gauss_norm", "gauss_norm", gauss, nsig)

### background
tau = RooRealVar("tau", "tau", -2.0, -5, -0.1)
exp = RooExponential("bkg","bkg", x, tau)
nbkg  = RooRealVar("nbkg", "nbkg", len(data), 0, len((data))*1.1)
exp_norm = RooExtendPdf("exp_norm", "exp_norm", exp, nbkg)

constraint_tau = RooGaussian("constraint_tau", "constraint_tau", tau, RooConst(-minuit_exp.values["lambda"]), RooConst(minuit_exp.errors["lambda"]))

### total
totpdf = RooAddPdf("totpdf","totpdf",RooArgList(gauss_norm,exp_norm))

#totpdf_c = RooAddPdf("totpdf","totpdf",RooArgList(gauss_norm,exp_norm))

totpdf_c = RooProdPdf("totpdf_c", "totpdf_c", RooArgList(totpdf, constraint_tau))

#ws.rfimport(totpdf)
ws.rfimport(totpdf_c)


ws.Print('V')

dataset = ws.data("data")
fitResult = totpdf_c.fitTo(dataset, ROOT.RooFit.Extended(), ROOT.RooFit.Minos(ROOT.kFALSE), ROOT.RooFit.Save(ROOT.kTRUE), ROOT.RooFit.Constrain(RooArgSet(tau)))


c = ROOT.TCanvas()
frame = x.frame(50)
dataset.plotOn( frame, ROOT.RooFit.Name('data_print'))
RemoveEmptyBins( frame, 'data_print')
totpdf_c.plotOn( frame, ROOT.RooFit.Name('model_print'))
frame.Draw()
Plot = ResidualPlot('title1', frame)
Plot.addResidual( 'data_print', 'model_print', 0.1, 3.0)
Plot.plot()
Plot.canvas.GetListOfPrimitives().At(0).cd()
c.Draw()


ws.defineSet('POI', "nsig")
ws.defineSet('OBS', 'x')
ws.defineSet('NUI', 'nbkg,tau')

conf = RooStats.ModelConfig('model', ws)
conf.SetPdf(ws.pdf('totpdf_c'))
conf.SetParametersOfInterest(ws.set('POI'))
conf.SetObservables(ws.set('OBS'))
conf.SetNuisanceParameters(ws.set('NUI'))

POI = ws.set('POI')
    
poi = POI.first()

    
#S+B model
model_sb = conf
model_sb.SetName("MODEL_SB")
#poi.setVal(35)
model_sb.SetSnapshot(RooArgSet(poi))
    
#BKG only 
model_b = conf.Clone()
model_b.SetName("MODEL_B")
oldval = poi.getVal()
poi.setVal(0)
model_b.SetSnapshot( RooArgSet(poi) )

#poi.setVal(oldval)
    
ws.rfimport(model_sb)
ws.rfimport(model_b)


data = ws.data("data")
model_sb = ws.obj('MODEL_SB')
model_b = ws.obj('MODEL_B')
    
data.Print()
model_b.Print()
model_sb.Print()

#Execution
calc = ROOT.RooStats.FrequentistCalculator(data, model_b, model_sb)
calc.SetToys(1000,1000)

#calc = ROOT.RooStats.AsymptoticCalculator(data, model_b, model_sb)
#calc = ROOT.RooStats.AsymptoticCalculator(data, model_sb, model_b)
#calc.SetOneSided(True)
#calc.SetQTilde(False)
#calc.SetPrintLevel(0)
#calc.SetOneSidedDiscovery(True) 

#res = calc.GetHypoTest()
#res = ROOT.RooStats.HypoTestInverter(calc)
#res.Print()

test = RooStats.HypoTestInverter(calc)
test.SetConfidenceLevel(0.95)
test.UseCLs(True)
    
#toysmc = test.GetHypoTestCalculator().GetTestStatSampler()
#RooStats.ProfileLikelihoodTestStat.SetAlwaysReuseNLL(True)
#profil = RooStats.ProfileLikelihoodTestStat(model_sb.GetPdf())
#profil.SetOneSided(True)
#toysmc.SetTestStatistic(profil)

test.SetFixedScan(15, 0.1, 25)
r = test.GetInterval()
r.Print()

plot = RooStats.HypoTestInverterPlot("alla","blabal", r)
c = ROOT.TCanvas("Scan")
plot.Draw("CLb 2CL")
c.Draw()

print("\n \n")
print("Obs upper limit {0}".format(r.UpperLimit()))
print("Exp upper limit {0}".format(r.GetExpectedUpperLimit(0)))
print("Exp upper limit 1sigma {0}".format(r.GetExpectedUpperLimit(1)))
print("Exp upper limit 2sigma {0}".format(r.GetExpectedUpperLimit(2)))
print("Exp upper limit -1sigma {0}".format(r.GetExpectedUpperLimit(-1)))
print("Exp upper limit -2sigma {0}".format(r.GetExpectedUpperLimit(-2)))