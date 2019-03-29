import pytest
from sklearn.datasets import make_blobs
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC

from optuna import distributions
from optuna import integration
from optuna import samplers


@pytest.mark.filterwarnings('ignore::UserWarning')
def test_fit():
    # type: () -> None

    X, y = make_blobs(n_samples=10)
    est = LinearSVC()
    param_dist = {'C': distributions.LogUniformDistribution(1e-04, 1e+03)}
    sampler = samplers.TPESampler(seed=0)
    tpe_search = integration.OptunaSearchCV(
        est,
        param_dist,
        cv=3,
        error_score='raise',
        max_iter=5,
        sampler=sampler
    )

    with pytest.raises(NotFittedError):
        tpe_search._check_is_fitted()

    tpe_search.fit(X, y)
    tpe_search._check_is_fitted()


@pytest.mark.filterwarnings('ignore::UserWarning')
def test_fit_with_pruning():
    # type: () -> None

    X, y = make_blobs(n_samples=10)
    est = SGDClassifier(max_iter=5, tol=1e-03)
    param_dist = {'alpha': distributions.LogUniformDistribution(1e-04, 1e+03)}
    sampler = samplers.TPESampler(seed=0)
    tpe_search = integration.OptunaSearchCV(
        est,
        param_dist,
        cv=3,
        enable_pruning=True,
        error_score='raise',
        max_iter=5,
        sampler=sampler
    )

    with pytest.raises(NotFittedError):
        tpe_search._check_is_fitted()

    tpe_search.fit(X, y)
    tpe_search._check_is_fitted()