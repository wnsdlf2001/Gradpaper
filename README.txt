1. �ʿ��� package list

	1) from collections import defaultdict (collection package�� defaultdict)

	2) import numpy (numpy package)

	3) import random (random package)


runConsole.py

2. �⺻ setting values :

	1) self.trainingData - ������ dataset�� �Է�

	2) self.label - output value �� ��ġ�� Index

	3) self.iternum - lamstar �� Ʈ���̴� Ƚ��

	4) self.distanceThreshold - input data�� node weight ���� distance value(���� ���� node�� ���� �������)

	5) self.subwordnumber - dataset�� ���� subword�� ����

inputdata.py.getSubwords()

3. �߰� setting values : 

	1) divnum - data�� ���� subword �� ����
	
	2) �� ���ĺ��� ��� �� subword�� ũ�⸦ ����

	3) �����ϴٸ� elif ���� �߰��Ͽ� �ϼ�


4. ���� 
	1) self.trainingData �� ���� subword�� ����

	2) runConsole.py�� �����Ͽ� �ڵ� ����

 