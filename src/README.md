# Online voting using Blind Signatures

The model of online voting we have implemented relies on the use of blind signatures to dissociate voter preference from vote identity.



The voting is done through a client server system built using the bottle framework in python. The server can implement mulitple ballot boxes (as pickle files) corresponding to different elections at the same time. Inorder to facilitate this, the server has been built to allow safe multi-threaded execution. All the voter needs to do is input his/her credential and candidate preference in the client program and it will take care of the authentication of the user and subsequent casting of the vote in the chosen ballot box. 

---

## Source files

The web framework used is bottle and most of the cryptographic function are imported from python libraries like hashlib, Hash and PublicKey from Crypto module

1. user.py, it is the client part of the system. It takes voter id, preference and ballot box as input from the voter. It then looks up the public key corresponding to given ballot box and blinds the preference.  The blinded preference is sent to the authenticator for signing along with the Voter identification. After successful reciept of the signed blinded preference the preference is unblinded and sent to the ballot box along with the unsigned preference. It also allows for the download of all votes cast in a particular ballot box for public verification of the election result.
2. server.py, it does the role of both the authenticator and of verifying the vote to be cast in the ballot box. As the authenticator, it creates and stores the public keys and private keys corresponding to each ballot box as pickled objects in corresponding files. It also performs the role verifying the signature on the preference when the vote is cast. The timestamp on the signed preference prevents recasting the same vote as different votes. It provides functionalities to calculate election results and also to download votes cast in a particular ballot.
3. utils.py contain commonly used function like creation and reading ballot boxes, pickling and unpickling, voter and vote verification  and logging
4. resource.py contains classes that provide abstractions for the different players in the system i.e., the authority who creates the ballot box, the verifier who checks for correct signature on the vote and the blinder who blindes candidate preference

Before you move on, go ahead and explore the repository. You've already seen the **Source** page, but check out the **Commits**, **Branches**, and **Settings** pages.

---

## Others

1. Files in the data/authority-objects contain authority objects (public and private keys) for each ballot boxes.
2. Files in the data/public-keys contain the public keys for each ballot boxes which are used by the client to blind the preference.
3. Files in the data/votes contain the votes cast in each ballot box
