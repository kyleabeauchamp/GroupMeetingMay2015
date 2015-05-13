from msmbuilder import example_datasets, cluster, msm, featurizer, lumping, utils, dataset, decomposition

figure_path = "/home/kyleb/src/kyleabeauchamp/GroupMeetingMay2015/figures/"

dt = 0.25

for tica_lagtime in [1, 400]:
    dih = dataset.NumpyDirDataset("./dihedrals/")
    X = dataset.dataset("./tica/tica%d.h5" % tica_lagtime)

    tica_model = utils.load("./tica/tica%d.pkl" % tica_lagtime)

    Xf = np.concatenate(X)

    figure()
    hexbin(Xf[:, 0], Xf[:, 1], bins='log')

    tica_model.timescales_

    title("TICA: lagtime %d (%.3f)" % (tica_lagtime, dt * tica_lagtime))
    xlabel("Slowest tIC")
    ylabel("Second Slowest tIC")
    savefig("%s/T4_tica_lag%d.png" % (figure_path, tica_lagtime), bbox_inches="tight")
