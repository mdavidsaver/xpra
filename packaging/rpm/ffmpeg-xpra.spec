%define _build_id_links none
%define _disable_source_fetch 0
%global __requires_exclude ^libx264.so.*$

%define libva 1
%if 0%{?el9}
%ifarch aarch64
%define libva 0
%endif
%endif

%global   real_name ffmpeg
Name:	     ffmpeg-xpra
Version:     5.0
Release:     1%{?dist}
Summary:     ffmpeg libraries for xpra

Group:       Applications/Multimedia
License:     GPL
URL:	     http://www.ffmpeg.org
Source0:     http://www.ffmpeg.org/releases/ffmpeg-%{version}.tar.xz
BuildRoot:   %(mktemp -ud %{_tmppath}/%{real_name}-%{version}-%{release}-XXXXXX)
AutoProv:    0
AutoReq:     0
%if 0%{?libva}
Requires:    libva
%endif
Requires:    x264-xpra

BuildRequires:	x264-xpra-devel
%if 0%{?libva}
BuildRequires:	libva-devel
%endif
BuildRequires:	nasm
BuildRequires:	make
BuildRequires:	gcc

%description
ffmpeg libraries for xpra


%package devel
Summary:   Development package for %{real_name}
Group:     Development/libraries
Requires:  %{name} = %{version}-%{release}
Requires:  pkgconfig
Requires:  ffmpeg-xpra = %{version}
%if 0%{?libva}
Requires:  libva
%endif
AutoReq:   0

%description devel
This package contains the development files for %{name}.


%prep
sha256=`sha256sum %{SOURCE0} | awk '{print $1}'`
if [ "${sha256}" != "51e919f7d205062c0fd4fae6243a84850391115104ccf1efc451733bc0ac7298" ]; then
	echo "invalid checksum for %{SOURCE0}"
	exit 1
fi
%setup -q -n %{real_name}-%{version}


%build
# set pkg_config_path for xpra video libs
PKG_CONFIG_PATH=%{_libdir}/xpra/pkgconfig ./configure \
	--prefix="%{_prefix}" \
	--libdir="%{_libdir}/xpra" \
	--shlibdir="%{_libdir}/xpra" \
	--mandir="%{_mandir}/xpra" \
	--incdir="%{_includedir}/xpra" \
	--extra-cflags="-I%{_includedir}/xpra" \
	--extra-ldflags="-L%{_libdir}/xpra" \
	--enable-runtime-cpudetect \
	--disable-avdevice \
	--enable-pic \
	--disable-zlib \
	--disable-filters \
	--disable-everything \
	--disable-doc \
	--disable-programs \
	--disable-libxcb \
	--enable-libx264 \
	--enable-libvpx \
%if 0%{?libva}
	--enable-vaapi \
%endif
	--enable-gpl \
	--enable-protocol=file \
	--enable-decoder=h264 \
	--enable-decoder=hevc \
	--enable-decoder=vp8 \
	--enable-decoder=vp9 \
	--enable-decoder=mpeg4 \
	--enable-decoder=mpeg1video \
	--enable-decoder=mpeg2video \
	--enable-encoder=libvpx_vp8 \
	--enable-encoder=libvpx_vp9 \
	--enable-encoder=mpeg4 \
	--enable-encoder=mpeg1video \
	--enable-encoder=mpeg2video \
	--enable-encoder=libx264 \
	--enable-encoder=aac \
%if 0%{?libva}
	--enable-encoder=h264_vaapi \
	--enable-encoder=hevc_vaapi \
	--enable-encoder=mpeg2_vaapi \
	--enable-encoder=vp8_vaapi \
	--enable-encoder=vp9_vaapi \
%endif
	--enable-muxer=mp4 \
	--enable-muxer=webm \
	--enable-muxer=matroska \
	--enable-muxer=ogg \
	--enable-demuxer=h264 \
	--enable-demuxer=hevc \
	--enable-demuxer=m4v \
	--enable-demuxer=matroska \
	--enable-demuxer=ogg \
%if 0%{?libva}
	--enable-hwaccel=h264_vaapi \
	--enable-hwaccel=hevc_vaapi \
	--enable-hwaccel=mpeg2_vaapi \
	--enable-hwaccel=vp8_vaapi \
	--enable-hwaccel=vp9_vaapi \
%endif
	--enable-pthreads \
	--enable-shared \
	--enable-debug \
	--disable-stripping \
	--disable-symver \
	--enable-rpath
	#--enable-static

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
#we don't care about the examples,
#and we can't turn them off using a build switch,
#so just delete them
rm -fr %{buildroot}/usr/share/ffmpeg/examples

#%post -p /sbin/ldconfig
#%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING* CREDITS
%{_libdir}/xpra/libavcodec.so.*
%{_libdir}/xpra/libavfilter.so.*
%{_libdir}/xpra/libavformat.so.*
%{_libdir}/xpra/libavutil.so.*
%{_libdir}/xpra/libpostproc.so.*
%{_libdir}/xpra/libswresample.so.*
%{_libdir}/xpra/libswscale.so.*


%files devel
%doc MAINTAINERS doc/APIchanges
%defattr(-,root,root,-)
%{_includedir}/xpra/libavcodec/
%{_includedir}/xpra/libavfilter/
%{_includedir}/xpra/libavformat/
%{_includedir}/xpra/libavutil/
%{_includedir}/xpra/libpostproc/
%{_includedir}/xpra/libswresample/
%{_includedir}/xpra/libswscale/
%{_libdir}/xpra/libavcodec.a
%{_libdir}/xpra/libavfilter.a
%{_libdir}/xpra/libavformat.a
%{_libdir}/xpra/libavutil.a
%{_libdir}/xpra/libpostproc.a
%{_libdir}/xpra/libswresample.a
%{_libdir}/xpra/libswscale.a
%{_libdir}/xpra/libavcodec.so
%{_libdir}/xpra/libavfilter.so
%{_libdir}/xpra/libavformat.so
%{_libdir}/xpra/libavutil.so
%{_libdir}/xpra/libpostproc.so
%{_libdir}/xpra/libswresample.so
%{_libdir}/xpra/libswscale.so
%{_libdir}/xpra/pkgconfig/libavcodec.pc
%{_libdir}/xpra/pkgconfig/libavfilter.pc
%{_libdir}/xpra/pkgconfig/libavformat.pc
%{_libdir}/xpra/pkgconfig/libavutil.pc
%{_libdir}/xpra/pkgconfig/libpostproc.pc
%{_libdir}/xpra/pkgconfig/libswresample.pc
%{_libdir}/xpra/pkgconfig/libswscale.pc


%changelog
* Sat Jan 15 2022 Antoine Martin <antoine@xpra.org> 5.0-1
- new upstream release

* Wed Dec 15 2021 Antoine Martin <antoine@xpra.org> 4.4.1-3
- force rebuild against updated libx264 (again - x264 did not build)

* Tue Dec 14 2021 Antoine Martin <antoine@xpra.org> 4.4.1-2
- force rebuild against updated libx264

* Tue Nov 02 2021 Antoine Martin <antoine@xpra.org> 4.4.1-1
- new upstream release

* Mon May 24 2021 Antoine Martin <antoine@xpra.org> 4.4-1
- new upstream release

* Wed Feb 17 2021 Antoine Martin <antoine@xpra.org> 4.3.1-5
- verify source checksum

* Sun Jan 10 2021 Antoine Martin <antoine@xpra.org> 4.3.1-4
- force rebuild against updated libx264

* Sat Jan 02 2021 Antoine Martin <antoine@xpra.org> 4.3.1-3
- manually handle dependencies in the main package

* Tue Nov 10 2020 Antoine Martin <antoine@xpra.org> 4.3.1-2
- add dependency on libva

* Sat Aug 22 2020 Antoine Martin <antoine@xpra.org> 4.3.1-1
- new upstream release

* Mon Jul 06 2020 Antoine Martin <antoine@xpra.org> 4.3-2
- rebuild against 10-bit x264
- remove autoreq / autoprov

* Wed Jun 17 2020 Antoine Martin <antoine@xpra.org> 4.3-1
- new upstream release

* Tue May 26 2020 Antoine Martin <antoine@xpra.org> 4.2.3-1
- new upstream release

* Mon Jan 20 2020 Antoine Martin <antoine@xpra.org> 4.2.2-1
- new upstream release

* Tue Sep 24 2019 Antoine Martin <antoine@xpra.org> 4.2.1-1
- new upstream release

* Thu Aug 08 2019 Antoine Martin <antoine@xpra.org> 4.2-1
- new upstream release

* Fri Jul 19 2019 Antoine Martin <antoine@xpra.org> 4.1.4-1
- new upstream release

* Tue Apr 16 2019 Antoine Martin <antoine@xpra.org> 4.1.3-1
- new upstream release

* Thu Mar 07 2019 Antoine Martin <antoine@xpra.org> 4.1.1-1
- new upstream release

* Thu Jan 10 2019 Antoine Martin <antoine@xpra.org> 4.1-2
- force rebuild

* Mon Nov 19 2018 Antoine Martin <antoine@xpra.org> 4.1-1
- new upstream release

* Mon Nov 05 2018 Antoine Martin <antoine@xpra.org> 4.0.3-1
- new upstream release

* Thu Aug 02 2018 Antoine Martin <antoine@xpra.org> 4.0.2-1
- new upstream release

* Wed Jun 20 2018 Antoine Martin <antoine@xpra.org> 4.0.1-1
- new upstream release

* Sat May 12 2018 Antoine Martin <antoine@xpra.org> 4.0-2
- enable mpeg1

* Sat Apr 21 2018 Antoine Martin <antoine@xpra.org> 4.0-1
- new upstream release

* Sun Mar 18 2018 Antoine Martin <antoine@xpra.org> 3.4.2-1
- new upstream release

* Wed Dec 13 2017 Antoine Martin <antoine@xpra.org> 3.4.1-1
- new upstream release

* Sat Oct 21 2017 Antoine Martin <antoine@xpra.org> 3.4-1
- new upstream release

* Thu Sep 14 2017 Antoine Martin <antoine@xpra.org> 3.3.4-1
- new upstream release

* Tue Aug 01 2017 Antoine Martin <antoine@xpra.org> 3.3.3-1
- new upstream release

* Sun Jun 11 2017 Antoine Martin <antoine@xpra.org> 3.3.2-1
- new upstream release

* Mon May 15 2017 Antoine Martin <antoine@xpra.org> 3.3.1-1
- new upstream release

* Tue Apr 18 2017 Antoine Martin <antoine@xpra.org> 3.3-3
- use xpra's PKG_CONFIG_PATH

* Tue Apr 18 2017 Antoine Martin <antoine@xpra.org> 3.3-2
- enable rpath

* Fri Apr 14 2017 Antoine Martin <antoine@xpra.org> 3.3-1
- new upstream release

* Mon Feb 13 2017 Antoine Martin <antoine@xpra.org> 3.2.4-1
- new upstream release

* Fri Dec 09 2016 Antoine Martin <antoine@xpra.org> 3.2.2-1
- new upstream release

* Sun Nov 27 2016 Antoine Martin <antoine@xpra.org> 3.2.1-1
- new upstream release

* Fri Nov 04 2016 Antoine Martin <antoine@xpra.org> 3.2-2
- add aac encoder for html5 client

* Sun Oct 30 2016 Antoine Martin <antoine@xpra.org> 3.2-1
- new upstream release

* Sun Oct 23 2016 Antoine Martin <antoine@xpra.org> 3.1.5-1
- new upstream release

* Sun Oct 09 2016 Antoine Martin <antoine@xpra.org> 3.1.4-1
- new upstream release

* Sun Aug 28 2016 Antoine Martin <antoine@xpra.org> 3.1.3-1
- new upstream release

* Sat Aug 20 2016 Antoine Martin <antoine@xpra.org> 3.1.2-1
- new upstream release

* Fri Aug 05 2016 Antoine Martin <antoine@xpra.org> 3.1.1-2
- add file protocol for testing muxer

* Mon Jul 04 2016 Antoine Martin <antoine@xpra.org> 3.1.1-1
- new upstream release

* Mon Jun 27 2016 Antoine Martin <antoine@xpra.org> 3.1-2
- new upstream release

* Sun Jun 12 2016 Antoine Martin <antoine@xpra.org> 3.0.2-2
- include encoders and muxers for ffmpeg encoder

* Fri Apr 29 2016 Antoine Martin <antoine@xpra.org> 3.0.2-1
- new upstream release

* Fri Apr 01 2016 Antoine Martin <antoine@xpra.org> 3.0.1-1
- new upstream release
- include mpeg4, ogg, matroska and webm support

* Mon Feb 15 2016 Antoine Martin <antoine@xpra.org> 3.0-1
- new upstream release

* Sat Feb 06 2016 Antoine Martin <antoine@xpra.org> 2.8.6-1
- new upstream release

* Thu Jan 21 2016 Antoine Martin <antoine@xpra.org> 2.8.5-1
- new upstream release

* Sun Dec 20 2015 Antoine Martin <antoine@xpra.org> 2.8.4-1
- new upstream release

* Sun Nov 29 2015 Antoine Martin <antoine@xpra.org> 2.8.3-1
- new upstream release

* Tue Nov 17 2015 Antoine Martin <antoine@xpra.org> 2.8.2-1
- new upstream release

* Fri Oct 16 2015 Antoine Martin <antoine@xpra.org> 2.8.1-1
- new upstream release

* Thu Sep 10 2015 Antoine Martin <antoine@xpra.org> 2.8-1
- new upstream release

* Tue Jul 28 2015 Antoine Martin <antoine@xpra.org> 2.7.2-1
- new upstream release

* Wed Jul 01 2015 Antoine Martin <antoine@xpra.org> 2.7.1-1
- new upstream release

* Wed Jun 10 2015 Antoine Martin <antoine@xpra.org> 2.7-1
- new upstream release

* Fri May 22 2015 Antoine Martin <antoine@xpra.org> 2.6.3-1
- new upstream release

* Sat Apr 04 2015 Antoine Martin <antoine@xpra.org> 2.6.1-1
- new upstream release

* Sat Apr 04 2015 Antoine Martin <antoine@xpra.org> 2.4.8-1
- new upstream release

* Tue Mar 10 2015 Antoine Martin <antoine@xpra.org> 2.4.7-1
- new upstream release

* Sun Jan 18 2015 Antoine Martin <antoine@xpra.org> 2.4.6-1
- new upstream release

* Mon Dec 29 2014 Antoine Martin <antoine@xpra.org> 2.4.5-1
- new upstream release

* Mon Dec 01 2014 Antoine Martin <antoine@xpra.org> 2.4.4-1
- new upstream release

* Mon Nov 03 2014 Antoine Martin <antoine@xpra.org> 2.4.3-1
- new upstream release

* Tue Oct 07 2014 Antoine Martin <antoine@xpra.org> 2.4.2-1
- new upstream release

* Sun Sep 21 2014 Antoine Martin <antoine@xpra.org> 2.4-1
- new upstream release

* Mon Aug 18 2014 Antoine Martin <antoine@xpra.org> 2.3.3-1
- version bump

* Thu Aug 07 2014 Antoine Martin <antoine@xpra.org> 2.3.2-1
- version bump, switch to 2.3.x

* Thu Aug 07 2014 Antoine Martin <antoine@xpra.org> 2.2.6-1
- version bump

* Thu Jul 31 2014 Antoine Martin <antoine@xpra.org> 2.2.5-1
- version bump

* Sun Jul 20 2014 Antoine Martin <antoine@xpra.org> 2.2.4-1
- version bump

* Mon Jul 14 2014 Matthew Gyurgyik <pyther@pyther.net>
- initial package
