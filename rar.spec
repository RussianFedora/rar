%define debug_package %{nil}

Summary:    Utility for creation RAR archives
Summary(ru):Утилита для создания архивов RAR
Name:       rar
Version:    5.1.1
Release:    2%{dist}
Epoch:      1

License:    Proprietary
Group:      Applications/Archiving
URL:        http://www.rarlab.com/download.htm
Source0:    http://www.rarlab.com/%{name}/%{name}linux-x64-%{version}.tar.gz
Source1:    http://www.rarlab.com/%{name}/%{name}linux-%{version}.tar.gz
Source2:    Permission_to_distribute_RAR.mbox
Source3:    %{name}.1
Source4:    unrar.1

Requires:   %{name}-docs = %{epoch}:%{version}-%{release}

ExclusiveArch:    x86_64 i686

%description
RAR is a console application allowing to manage archive files in command line
mode. RAR provides compression, encryption, data recovery and some other
functions.

RAR supports only RAR format archives, which have *.rar file name extension by
default. ZIP and other formats are not supported.

%description -l ru
RAR — это консольное приложение, позволяющее оперировать с файлами архивов в
режиме командной строки. RAR предоставляет возможность сжатия, шифрования,
восстановления данных, а также некоторые другие функции.

RAR поддерживает работу только с архивами в собственном формате, по умолчанию
имеющими расширение *.rar. ZIP и остальные форматы не поддерживаются.

%package    docs
Summary:    Necessary documentation for distribution RAR archiver
Summary(ru):Необходимая для распространиения архиватора RAR документация
Group:      Applications/Archiving
BuildArch:  noarch

%description docs
This package contains necessary documentation for distribution RAR archiver

%description docs -l ru
Этот пакет содержит необходимую для распространиения архиватора RAR документацию

%package -n unrar
Summary:    Utility for extracting, testing and viewing RAR archives
Summary(ru):Утилита для распаковки, проверки и просмотра содержимого архивов RAR
Group:      Applications/Archiving
Requires:   %{name}-docs = %{epoch}:%{version}-%{release}

%description -n unrar
The UNRAR utility is a freeware program for extracting, testing and viewing the
contents of archives created with the RAR archiver version 1.50 and above.

%description -n unrar -l ru
Утилита UNRAR — это бесплатное приложение для распаковки, проверки и просмотра
содержимого архивов, созданных архиватором RAR версий 1.5 и выше.

%prep
%setup -q -c -T

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

pushd %{buildroot}
    %ifarch x86_64
        gzip -dkc %{SOURCE0} > %{name}-%{version}.tar
    %else
        gzip -dkc %{SOURCE1} > %{name}-%{version}.tar
    %endif

    tar -xf %{name}-%{version}.tar
popd

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_defaultdocdir}/%{name}-%{version}
mkdir -p %{buildroot}%{_mandir}/man1

# Install RAR files
pushd %{buildroot}/%{name}
    install -pm 755 %{name} %{buildroot}%{_bindir}/%{name}
    install -pm 755 unrar %{buildroot}%{_bindir}/unrar
    install -pm 755 default.sfx %{buildroot}%{_libdir}/default.sfx
    install -pm 644 rarfiles.lst %{buildroot}%{_sysconfdir}/rarfiles.lst
    install -pm 644 %{SOURCE2} %{buildroot}%{_defaultdocdir}/%{name}-%{version}/Permission_to_distribute_RAR.mbox
    install -pm 644 acknow.txt %{buildroot}%{_defaultdocdir}/%{name}-%{version}/acknow.txt
    install -pm 644 license.txt %{buildroot}%{_defaultdocdir}/%{name}-%{version}/license.txt
    install -pm 644 order.htm %{buildroot}%{_defaultdocdir}/%{name}-%{version}/order.htm
    install -pm 644 rar.txt %{buildroot}%{_defaultdocdir}/%{name}-%{version}/rar.txt
    install -pm 644 readme.txt %{buildroot}%{_defaultdocdir}/%{name}-%{version}/readme.txt
    install -pm 644 whatsnew.txt %{buildroot}%{_defaultdocdir}/%{name}-%{version}/whatsnew.txt
    cp -p %{SOURCE3} %{name}.1
    cp -p %{SOURCE4} unrar.1
    sed -e 's|_path_|%{_defaultdocdir}/%{name}-%{version}|g' -i %{name}.1
    sed -e 's|_path_|%{_defaultdocdir}/%{name}-%{version}|g' -i unrar.1
    gzip -c %{name}.1 > %{buildroot}%{_mandir}/man1/%{name}.1.gz
    gzip -c unrar.1 > %{buildroot}%{_mandir}/man1/unrar.1.gz
    chmod 644 %{buildroot}%{_mandir}/man1/%{name}.1.gz
    chmod 644 %{buildroot}%{_mandir}/man1/unrar.1.gz
popd

# Remove unused directory and tarball:
pushd %{buildroot}
    rm %{name}-%{version}.tar
    rm -rf %{buildroot}/rar
popd

%post

%preun

%files
%{_bindir}/%{name}
%{_libdir}/default.sfx
%config %{_sysconfdir}/rarfiles.lst
%doc %{_mandir}/man1/%{name}.1.gz

%files docs
%doc %{_defaultdocdir}/*

%files -n unrar
%{_bindir}/unrar
%doc %{_mandir}/man1/unrar.1.gz

%changelog
* Sun Sep 29 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5.1.1-2.R
- add <unrar> and <-docs> subpackages
- add <Epoch:1> for replacement too old <unrar> version from <rpmfusion> repo
- add RAR and UNRAR manual pages
- clean up *.spec file

* Sun Sep 21 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 5.1.1-1.R
- initial build for Fedora
