1. 필요한 package list

	1) from collections import defaultdict (collection package의 defaultdict)

	2) import numpy (numpy package)

	3) import random (random package)


runConsole.py

2. 기본 setting values :

	1) self.trainingData - 적용할 dataset을 입력

	2) self.label - output value 가 위치한 Index

	3) self.iternum - lamstar 모델 트레이닝 횟수

	4) self.distanceThreshold - input data와 node weight 간의 distance value(높을 수록 node가 적게 만들어짐)

	5) self.subwordnumber - dataset에 대한 subword의 갯수

inputdata.py.getSubwords()

3. 추가 setting values : 

	1) divnum - data를 나눌 subword 의 갯수
	
	2) 각 알파벳에 등분 할 subword의 크기를 지정

	3) 부족하다면 elif 문을 추가하여 완성


4. 실행 
	1) self.trainingData 에 맞춰 subword를 결정

	2) runConsole.py를 실행하여 코드 실행

 