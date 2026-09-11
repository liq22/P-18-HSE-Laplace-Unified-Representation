"""Counterexamples and objective-specific posterior approximation checks."""
import unittest
import numpy as np
from experiments.sampled_conditioning.parameterization_controls import (
    blocks, bounds, representations, kl, lowrank_covariance, denoiser_gap)

class ParameterizationTests(unittest.TestCase):
    def setUp(self):
        self.j=.2*np.eye(6)+2*np.ones((6,6))
        self.h=np.array([1.,-.3,.4,.7,-.8,.2])
        self.groups=((0,1,2,3),(4,5))

    def test_product_projection_decomposition_and_schur(self):
        arms=representations(self.j,self.h,self.groups)
        mu,s,_=arms['full'];mn,sn,_=arms['natural_blocks'];mm,sm,_=arms['moment_blocks']
        difference=kl(mu,s,mn,sn)-kl(mu,s,mm,sm)
        marginal_sum=sum(kl(mu[list(g)],s[np.ix_(g,g)],mn[list(g)],sn[np.ix_(g,g)]) for g in self.groups)
        np.testing.assert_allclose(difference,marginal_sum,atol=1e-12)
        np.testing.assert_allclose(kl(mu,s,mm,sm),.5526618616280481,atol=1e-12)
        for g in self.groups:
            self.assertGreaterEqual(np.linalg.eigvalsh((s-sn)[np.ix_(g,g)]).min(),-1e-12)
        self.assertEqual(arms['natural_blocks'][2],arms['moment_blocks'][2])

    def test_joint_error_cancellation_and_amplification(self):
        q=np.eye(2);qt=np.array([[2.,.3],[.3,1.5]]);h=np.array([1.,2.]);e=qt-q
        cancel=bounds(q,h,qt,h+e@h);amplify=bounds(q,h,qt,h-e@h)
        np.testing.assert_allclose(cancel['mean_residual_squared'],0.,atol=1e-12)
        self.assertGreater(amplify['exact_kl'],cancel['exact_kl'])

    def test_tighter_bound_on_noncommuting_spd_pairs(self):
        rng=np.random.default_rng(1213)
        for _ in range(100):
            a,b=rng.normal(size=(4,4)),rng.normal(size=(4,4))
            result=bounds(a@a.T+np.eye(4),rng.normal(size=4),b@b.T+np.eye(4),rng.normal(size=4))
            self.assertLessEqual(result['exact_kl'],result['tight_bound']+1e-8)
            self.assertLessEqual(result['tight_bound'],result['old_bound']+1e-8)

    def test_goal_ranking_can_reverse(self):
        s=np.eye(2);mu=np.zeros(2);a=np.array([0.,.9]);b=np.array([1.,0.]);l=np.array([[0.,1.]])
        self.assertLess(kl(mu,s,a,s),kl(mu,s,b,s))
        self.assertGreater(kl(l@mu,l@s@l.T,l@a,l@s@l.T),kl(l@mu,l@s@l.T,l@b,l@s@l.T))

    def test_phase_covariance_including_nonisotropic_prior(self):
        rng=np.random.default_rng(13);x=rng.normal(size=(6,6));j=x@x.T+np.eye(6)
        q0=np.diag([1.,2.,3.,4.,5.,6.]);h0=rng.normal(size=6);b=rng.normal(size=6)
        u=np.zeros((6,6))
        for k,angle in enumerate([.2,.9,-.7]):
            c,s=np.cos(angle),np.sin(angle);u[2*k:2*k+2,2*k:2*k+2]=[[c,-s],[s,c]]
        np.testing.assert_allclose(blocks(u@j@u.T,self.groups),u@blocks(j,self.groups)@u.T,atol=1e-12)
        q=q0+blocks(j,self.groups);qp=u@q0@u.T+blocks(u@j@u.T,self.groups)
        np.testing.assert_allclose(np.linalg.solve(qp,u@(h0+b)),u@np.linalg.solve(q,h0+b),atol=1e-12)
        iso=lambda a: np.diag(np.repeat([np.trace(a[k:k+2,k:k+2])/2 for k in range(0,6,2)],2))
        np.testing.assert_allclose(iso(u@j@u.T),u@iso(j)@u.T,atol=1e-12)
        self.assertGreater(np.linalg.norm(np.diag(np.diag(u@j@u.T))-u@np.diag(np.diag(j))@u.T),.1)

    def test_lowrank_full_rank_recovers_covariance(self):
        s=np.linalg.solve(np.eye(6)+self.j,np.eye(6))
        np.testing.assert_allclose(lowrank_covariance(np.eye(6),s,6),s,atol=1e-12)
        np.testing.assert_allclose(lowrank_covariance(np.eye(6),s,0),np.eye(6),atol=1e-12)

    def test_gaussian_denoiser_gap_against_monte_carlo(self):
        mu=np.array([.2,-.3]);mq=np.array([-.1,.4]);v=np.array([[.8,.2],[.2,.5]]);w=np.diag([.6,1.2]);a,s=.8,.6
        m=a*a*v+s*s*np.eye(2);n=a*a*w+s*s*np.eye(2)
        rng=np.random.default_rng(2);z=rng.multivariate_normal(a*mu,m,size=100000)
        exact=s*np.linalg.solve(m,(z-a*mu).T).T
        approximate=s*np.linalg.solve(n,(z-a*mq).T).T
        losses=np.sum((exact-approximate)**2,axis=1)
        self.assertLess(abs(losses.mean()-denoiser_gap(mu,v,mq,w,a,s)),5*losses.std(ddof=1)/np.sqrt(len(losses)))
        self.assertAlmostEqual(denoiser_gap(mu,v,mq,w,0.,1.),0.)

if __name__=='__main__':
    unittest.main()
