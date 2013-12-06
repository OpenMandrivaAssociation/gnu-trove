# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
%define gcj_support 1
%define section devel
%define short_name trove

Summary:        High performance collections for Java
Name:           gnu-%{short_name}
Epoch:          0
Version:        1.0.2
Release:        10
License:        LGPL
Group:          Development/Java
Url:            http://trove4j.sourceforge.net/
Source0:        trove-1.0.2.tar.gz
Source1:        trove-build.xml
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit >= 0:1.6
BuildRequires:  junit
BuildRequires:  locales-en
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
Provides:       gnu.trove = %{epoch}:%{version}-%{release}
Obsoletes:      gnu.trove < %{epoch}:%{version}-%{release}

%description
The GNU Trove library has two objectives: 

Provide "free" (as in "free speech" and "free beer"), 
fast, lightweight implementations of the java.util 
Collections API. These implementations are designed 
to be pluggable replacements for their JDK equivalents. 

Whenever possible, provide the same collections support 
for primitive types. This gap in the JDK is often 
addressed by using the "wrapper" classes 
(java.lang.Integer, java.lang.Float, etc.) with 
Object-based collections. For most applications, however, 
collections which store primitives directly will require 
less space and yield significant performance gains. 


%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Provides:       gnu.trove-javadoc = %{epoch}:%{version}-%{release}
Obsoletes:      gnu.trove-javadoc < %{epoch}:%{version}-%{release}

%description javadoc
%{summary}.

%prep
%setup -q -n %{short_name}-%{version}
cp %{SOURCE1} build.xml

%build
export LC_ALL=ISO-8859-1
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=
%{ant} -Dbuild.sysclasspath=only dist

%install
# jars
mkdir -p %{buildroot}%{_javadir}
cp -p target/%{short_name}-%{version}.jar \
      %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done
ln -sf %{name}.jar gnu.trove.jar)

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name} # ghost symlink

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%doc LICENSE.txt
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif


%files javadoc
%doc %{_javadocdir}/%{name}
%doc %{_javadocdir}/%{name}-%{version}

