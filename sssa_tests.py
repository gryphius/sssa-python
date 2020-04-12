import unittest
from SSSA import sssa

class TestStringMethods(unittest.TestCase):
    def test_create_combine(self):
        values = ["N17FigASkL6p1EOgJhRaIquQLGvYV0", "0y10VAfmyH7GLQY6QccCSLKJi8iFgpcSBTLyYOGbiYPqOpStAf1OYuzEBzZR", "KjRHO1nHmIDidf6fKvsiXWcTqNYo2U9U8juO94EHXVqgearRISTQe0zAjkeUYYBvtcB8VWzZHYm6ktMlhOXXCfRFhbJzBUsXaHb5UDQAvs2GKy6yq0mnp8gCj98ksDlUultqygybYyHvjqR7D7EAWIKPKUVz4of8OzSjZlYg7YtCUMYhwQDryESiYabFID1PKBfKn5WSGgJBIsDw5g2HB2AqC1r3K8GboDN616Swo6qjvSFbseeETCYDB3ikS7uiK67ErIULNqVjf7IKoOaooEhQACmZ5HdWpr34tstg18rO"]
        minimum = [4, 6, 20]
        shares = [5, 100, 100]

        sss = sssa()

        for index,value in enumerate(values):
            self.assertEqual(sss.combine(sss.create(minimum[index], shares[index], value)), value)

    def test_library_combine(self):
        sss = sssa()
        shares = ["U1k9koNN67-og3ZY3Mmikeyj4gEFwK4HXDSglM8i_xc=yA3eU4_XYcJP0ijD63Tvqu1gklhBV32tu8cHPZXP-bk=", "O7c_iMBaGmQQE_uU0XRCPQwhfLBdlc6jseTzK_qN-1s=ICDGdloemG50X5GxteWWVZD3EGuxXST4UfZcek_teng=", "8qzYpjk7lmB7cRkOl6-7srVTKNYHuqUO2WO31Y0j1Tw=-g6srNoWkZTBqrKA2cMCA-6jxZiZv25rvbrCUWVHb5g=", "wGXxa_7FPFSVqdo26VKdgFxqVVWXNfwSDQyFmCh2e5w=8bTrIEs0e5FeiaXcIBaGwtGFxeyNtCG4R883tS3MsZ0=", "j8-Y4_7CJvL8aHxc8WMMhP_K2TEsOkxIHb7hBcwIBOo=T5-EOvAlzGMogdPawv3oK88rrygYFza3KSki2q8WEgs="]

        self.assertEqual(sss.combine(shares), "test-pass")

    def test_add_share(self):
        secret='the cake is a lie'
        sss = sssa()
        shares = sss.create(3,5,secret)
        self.assertEqual(len(shares),5)
        # restore secret using original shares
        self.assertEqual(sss.combine(shares[:3]),secret)
        # add new share and restore secret with a mix of original and new share
        new_shares = sss.add_share(shares)
        self.assertEqual(len(new_shares),6)
        self.assertEqual(sss.combine(new_shares[-3:]),secret)

if __name__ == '__main__':
    unittest.main()
