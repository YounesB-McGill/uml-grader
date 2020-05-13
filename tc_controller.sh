#!/usr/bin/env bash

# Large command to start TouchCore, obtained from Eclipse run configuration.
TC_CMD="/usr/local/jdk1.8.0_201/bin/java \
    -Dfile.encoding=UTF-8 \
    -classpath /media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.ram.gui/bin:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.ram.gui/lib/jogl/gluegen-rt.jar:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.ram.gui/lib/jogl/jogl-all.jar:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.ram.gui/lib/jgraphx.jar:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.ram.gui/lib:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.ram.gui/lib/mt4j.jar:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.ram.gui/lib/org.abego.treelayout.core.jar:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.ram.edit/bin:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.core.runtime_3.17.100.v20200203-0917.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.osgi_3.15.200.v20200214-1600.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.osgi.compatibility.state_1.1.700.v20200207-2156.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.equinox.common_3.11.0.v20200206-0817.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.core.jobs_3.10.700.v20200106-1020.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.equinox.registry_3.8.700.v20200121-1457.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.equinox.preferences_3.7.700.v20191213-1901.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.core.contenttype_3.7.600.v20200124-1609.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.equinox.app_1.4.400.v20191212-0743.jar:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.ram/bin:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.emf.ecore_2.21.0.v20200127-1342.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.emf.common_2.18.0.v20191225-1014.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.emf.ecore.xmi_2.16.0.v20190528-0725.jar:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/core/ca.mcgill.sel.core/bin:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/core/ca.mcgill.sel.commons/bin:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.uml2.uml.resources_5.5.0.v20200302-1312.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.uml2.uml_5.5.0.v20200302-1312.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.uml2.common_2.5.0.v20200302-1312.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.uml2.types_2.5.0.v20200302-1312.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.emf.mapping.ecore2xml_2.11.0.v20180706-1146.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.uml2.uml.profile.standard_1.5.0.v20200302-1312.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.ocl.ecore_3.15.0.v20200309-0848.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.ocl_3.15.0.v20200309-0848.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/lpg.runtime.java_2.0.17.v201004271640.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.ocl.common_1.8.400.v20200309-0848.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.ocl.xtext.oclinecore_1.11.0.v20200309-0848.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.ocl.xtext.essentialocl_1.11.0.v20200309-0848.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.ocl.xtext.base_1.11.0.v20200309-0848.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.ocl.pivot_1.11.0.v20200309-0848.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.jdt.annotation_2.2.400.v20191120-1313.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.emf.edit_2.16.0.v20190920-0401.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.emf.ecore.change_2.14.0.v20190528-0725.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.xtext_2.21.0.v20200302-1141.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.antlr.runtime_3.2.0.v201101311130.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/com.google.inject_3.0.0.v201605172100.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.emf.mwe.core_1.5.2.v20200224-0816.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.apache.commons.cli_1.2.0.v201404270220.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.emf.mwe2.runtime_2.11.2.v20200224-0816.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.emf.mwe.utils_1.5.2.v20200224-0816.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.xtext.util_2.21.0.v20200302-1141.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/com.google.guava_27.1.0.v20190517-1946.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/javax.inject_1.0.0.v20091030.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.ocl.xtext.oclstdlib_1.11.0.v20200309-0848.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.ocl.xtext.completeocl_1.11.0.v20200309-0848.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.apache.log4j_1.2.15.v201012070815.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.apache.commons.io_2.6.0.v20190123-2029.jar:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/core/ca.mcgill.sel.core.edit/bin:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/core/ca.mcgill.sel.core.controller/bin:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.ram.controller/bin:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.emf_2.8.0.v20180706-1146.jar:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/core/ca.mcgill.sel.core.weaver/bin:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/Compare/ca.mcgill.sel.mark/bin:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.junit_4.13.0.v20200204-1500.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.hamcrest.core_1.3.0.v20180420-1519.jar:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.ram.controller/tests/lib/assertj-core-3.5.1.jar:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.ram.weaver/bin:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.ram.classloader/bin:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.ram.classloader/lib/asm-5.0.3.jar:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.ram.generator/bin:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.acceleo.engine_3.7.10.202002210922.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.acceleo.common_3.7.10.202002210922.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.acceleo.model_3.7.10.202002210922.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.acceleo.profiler_3.7.10.202002210922.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.emf.codegen.ecore_2.21.0.v20200112-0705.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.emf.codegen_2.19.0.v20190821-1536.jar:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.ram.validator/bin:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/core/ca.mcgill.sel.core.evaluator/bin:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/core/ca.mcgill.sel.core.evaluator/lib/familiar-bridge-0.0.1.jar:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.ram.expressions/bin:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.xtext.xbase_2.21.0.v20200302-1201.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.xtext.common.types_2.21.0.v20200302-1201.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.xtend.lib_2.21.0.v20200302-1127.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.xtext.xbase.lib_2.21.0.v20200302-1127.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.xtend.lib.macro_2.21.0.v20200302-1127.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.xtext.junit4_2.21.0.v20200302-1241.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.xtext.xtext.generator_2.21.0.v20200302-1141.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.emf.mwe2.launch_2.11.2.v20200224-0816.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.emf.mwe2.language_2.11.2.v20200224-0816.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.emf.mwe2.lib_2.11.2.v20200224-0816.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.objectweb.asm_7.2.0.v20191010-1910.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.apache.commons.logging_1.2.0.v20180409-1502.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/com.ibm.icu_64.2.0.v20190507-1337.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.xtext.generator_2.21.0.v20200302-1201.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.xtend_2.2.0.v201605260315.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.xpand_2.2.0.v201605260315.jar:\
/media/Storage/McGill/Winter2020/ECSE694/eclipse/plugins/org.eclipse.xtend.typesystem.emf_2.2.0.v201605260315.jar:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.classdiagram/bin:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/core/ca.mcgill.sel.core.language/bin:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.classdiagram.edit/bin:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.classdiagram.controller/bin:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/Compare/ca.mcgill.sel.classroom/bin:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.ram.gui/lib/jawjaw-1.0.2.jar:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.ram.gui/lib/json-simple-1.1.1.jar:\
/media/Storage/McGill/Winter2020/ECSE694/touchcore-ws/touchram/ca.mcgill.sel.ram.gui/lib/ws4j-1.0.1.jar\
    ca.mcgill.sel.ram.ui.TouchCORE"

OUTPUT="tc_output_final2.txt"

STUDENT_CDM_LOC="out_final"

#rm -f $OUTPUT

# For simplicity, this script assumes the instructor solution is fixed.

#for i in {0..115}; do  # inclusive range
for i in 54 63 86 101; do
#for i in 20 36 47 61 70 71 80 82 92 97 101; do
    # Copy student solution i to correct place
    cp "$STUDENT_CDM_LOC/$i.cdm" "../tc-models/1k.cdm"
    echo -e "\nGRADING SUBMISSION $i\n" >> $OUTPUT
    echo -e "~~~~~~ GRADING SUBMISSION $i ~~~~~~\n"

    # start TouchCore in the background and save its process ID, so it can be stopped later
    $TC_CMD >> $OUTPUT &
    TC_PID=$!

    source /home/hp/.local/share/virtualenvs/uml-grader-Qi2_SrMR/bin/activate
    ./tc_gui_grader.py

    sleep 1s
    kill -9 $TC_PID
done
