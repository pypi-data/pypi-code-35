#
# script to run the wiggler preprocessor (created by ShadowOui:Wiggler)
#
from srxraylib.sources import srfunc

(traj, pars) = srfunc.wiggler_trajectory(
    b_from=0,
    inData="",
    nPer=50,
    nTrajPoints=501,
    ener_gev=6.04,
    per=0.04,
    kValue=7.85,
    trajFile="tmp.traj",
    shift_x_flag=0,
    shift_x_value=0.0,
    shift_betax_flag=0,
    shift_betax_value=0.0)

#
# calculate cdf and write file for Shadow/Source
#

srfunc.wiggler_cdf(traj,
                   enerMin=5000,
                   enerMax=100000,
                   enerPoints=1001,
                   outFile=b'/users/srio/OASYS1.1d/shadowOui/orangecontrib/shadow/widgets/sources/xshwig.sha',
                   elliptical=False)

#
# end script
#