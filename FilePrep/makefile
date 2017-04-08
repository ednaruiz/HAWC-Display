all: ordertime parse-extended-reco

ordertime: ordertime.cxx
	clang++ `hawc-config --cppflags --ldflags` -o order-time ordertime.cxx

parse-extended-reco: parse-extend-reco.cxx	
	clang++ `hawc-config --cppflags --ldflags` -o parse-extended-reco parse-extend-reco.cxx
