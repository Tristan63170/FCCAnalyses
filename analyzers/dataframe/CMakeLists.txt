
find_package(ROOT REQUIRED COMPONENTS ROOTDataFrame ROOTVecOps TMVA)
include(${ROOT_USE_FILE})
#include("${ROOT_DIR}/modules/RootNewMacros.cmake")


set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

get_target_property(EDM4HEP_INCLUDE_DIRS EDM4HEP::edm4hep INTERFACE_INCLUDE_DIRECTORIES)

include_directories(${EDM4HEP_INCLUDE_DIRS} 
		    ${podio_INCLUDE_DIR} 
                    ${FASTJET_INCLUDE_DIR} 
		    ${acts_INCLUDE_DIR}
		    ${AWKWARD_INCLUDE}
                    ${DELPHES_INCLUDE_DIR}
                    ${DELPHES_EXTERNALS_INCLUDE_DIR}
                    ${DELPHES_EXTERNALS_TKCOV_INCLUDE_DIR}
		    #${Boost_INCLUDE_DIRS}
		    )

message(STATUS "includes-------------------------- dataframe awkward: ${AWKWARD_INCLUDE}")
message(STATUS "includes-------------------------- dataframe edm4hep: ${EDM4HEP_INCLUDE_DIRS}")
message(STATUS "includes-------------------------- dataframe podio  : ${podio_INCLUDE_DIR}")
message(STATUS "includes-------------------------- dataframe fastjet: ${FASTJET_INCLUDE_DIRS}")
message(STATUS "includes-------------------------- dataframe delphes: ${DELPHES_INCLUDE_DIR}")
message(STATUS "includes-------------------------- dataframe delphes EXt: ${DELPHES_EXTERNALS_TKCOV_INCLUDE_DIR}")



ROOT_GENERATE_DICTIONARY(G__FCCAnalyses FCCAnalyses/dummyLoader.h
					FCCAnalyses/MCParticle.h
					FCCAnalyses/ReconstructedParticle.h
					FCCAnalyses/ReconstructedParticle2Track.h
					FCCAnalyses/ReconstructedParticle2MC.h
					FCCAnalyses/JetClustering.h
					FCCAnalyses/JetClusteringUtils.h
					FCCAnalyses/JetTaggingUtils.h
					FCCAnalyses/ValenciaPlugin.h
					FCCAnalyses/VertexingUtils.h
					FCCAnalyses/VertexFitterSimple.h
					FCCAnalyses/VertexFinderActs.h					
					FCCAnalyses/VertexFitterActs.h
					FCCAnalyses/myUtils.h
					FCCAnalyses/CaloNtupleizer.h
					LINKDEF FCCAnalyses/LinkDef.h)

file(GLOB sources *.cc)
file(GLOB headers *.h)
add_library(FCCAnalyses SHARED ${sources} ${headers} G__FCCAnalyses.cxx )
target_include_directories(FCCAnalyses  PUBLIC
                           ${CMAKE_SOURCE_DIR}/analyzers/dataframe
                           ${FCCEDM_INCLUDE_DIRS}
	                   ${FASTJET_INCLUDE_DIR}
		           ${acts_INCLUDE_DIR}
			   ${AWKWARD_INCLUDE}
			   ${DELPHES_INCLUDE_DIR}
			   ${DELPHES_EXTERNALS_INCLUDE_DIR}
                           ${DELPHES_EXTERNALS_TKCOV_INCLUDE_DIR})

target_link_libraries(FCCAnalyses 
                      ROOT::Physics 
		      ROOT::MathCore 
		      ROOT::ROOTVecOps
		      ROOT::ROOTDataFrame
		      ROOT::TMVA
		      EDM4HEP::edm4hep 
		      EDM4HEP::edm4hepDict 
		      podio::podio 
		      ${FASTJET_LIBRARY} fastjetplugins
		      ${acts_LIBRARY} ActsCore
                      Delphes
		      #${AWKWARD_LIBRARIES}
		      ${LIBAWKWARD}
		      ${CPU-KERNELS} ${LIBDL})




set_target_properties(FCCAnalyses PROPERTIES
  PUBLIC_HEADER "${headers}")

install(TARGETS FCCAnalyses
    RUNTIME DESTINATION "${INSTALL_BIN_DIR}" COMPONENT bin
    LIBRARY DESTINATION "${INSTALL_LIB_DIR}" COMPONENT shlib
    PUBLIC_HEADER DESTINATION "${INSTALL_INCLUDE_DIR}/FCCAnalyses"
    COMPONENT dev
    )

install(FILES
  "${PROJECT_BINARY_DIR}/analyzers/dataframe/libFCCAnalyses.rootmap"
    DESTINATION "${INSTALL_LIB_DIR}" COMPONENT dev)

if (${ROOT_VERSION} GREATER 6)
    install(FILES
          "${PROJECT_BINARY_DIR}/analyzers/dataframe/libFCCAnalyses_rdict.pcm"
                DESTINATION "${INSTALL_LIB_DIR}" COMPONENT dev)
    endif()
