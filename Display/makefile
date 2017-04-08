all: scan-showers

scan-showers: scan-showers.cxx
	clang++ `hawc-config --cppflags --ldflags` scan-showers.cxx -o scan-showers
