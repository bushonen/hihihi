#!/usr/local/bin/perl

#��������������������������������������������������������������������
#��  WEB ENQUETE v4.2 (2004/01/02)
#��  Copyright (c) KentWeb
#��  webmaster@kent-web.com
#��  http://www.kent-web.com/
#��������������������������������������������������������������������
$ver = 'WEB ENQUETE v4.2';
#��������������������������������������������������������������������
#�� [���ӎ���]
#�� 1. ���̃X�N���v�g�̓t���[�\�t�g�ł��B���̃X�N���v�g���g�p����
#��    �����Ȃ鑹�Q�ɑ΂��č�҂͈�؂̐ӔC�𕉂��܂���B
#�� 2. �ݒu�Ɋւ��鎿��̓T�|�[�g�f���ɂ��肢�������܂��B
#��    ���ڃ��[���ɂ�鎿��͈�؂��󂯂������Ă���܂���B
#��������������������������������������������������������������������
#
# �y�t�@�C���\����z
#
#  public_html (�z�[���f�B���N�g��)
#      |
#      +-- enq / enq.cgi    [705]
#           |    enq.log    [606]
#           |    axslog.cgi [606]
#           |    jcode.pl   [604]
#           |    graph.gif
#           |
#           +-- lock [707] /
#
# �y�`�F�b�N���[�h�Ăяo����z
#
#  http://www.xxx.xxx/enq/enq.cgi?mode=check
#

#-------------------------------------------------
#  ����{�ݒ�
#-------------------------------------------------

# ���C�u������荞��
require './jcode.pl';

# �^�C�g����
$title = "����Ƃ���A���P�[�g�@���̂P<br>�M���̎�ɂ����P�s�{";

# �^�C�g�������̐F
$t_color = "#444444";

# �^�C�g�������T�C�Y
$t_size = '20px';

# �{���̕����T�C�Y
$b_size = '13px';

# �{���̕����t�H���g
$b_face = "MS UI Gothic, Osaka";

# �X�N���v�gURL
$script = './collect.cgi';

# �f�[�^�t�@�C��
$logfile = './enq.log';

# �A�N�Z�X���O
$axslog = './axslog.cgi';

# �A�N�Z�X���O�̋L�^��
$logMax = 200;

# �Ǘ��p�p�X���[�h
$pass = 'azusawa3';

# ���[�U���ڒǉ��@�\�i���[�U�����R�ɍ��ڂ�ǉ��\�j
#  0 : ���Ȃ�
#  1 : ����i����IP�ɂ��A�������ǉ��s�ׂ͋֎~�j
#  2 : ����i����IP�ɂ��A�������ǉ��s�ׂ͉\�j
$freeitem = 0;

# �O���t�摜 (��΃p�X���� http://����)
$graph = "./graph.gif";

# �߂�� (��΃p�X���� http://����)
$home = "../../index.html";

# body�^�O
$body = '<body bgcolor="#ffffff" text="#111111">';

# �e�[�u�����u�^�C�g���v�Z���F
$tblCol1 = "#111111";	# �����F
$tblCol2 = "#ffffff";	# ���n�F

# �e�[�u�����u���ځv�Z���F
$tblCol3 = "#000000";	# �����F
$tblCol4 = "#ccffdd";	# ���n�F

# ���b�N�t�@�C���@�\ (0=no 1=yes)
$lockkey = 0;

# ���b�N�t�@�C����
$lockfile = './lock/enq.lock';

# ���[�̉񓚌`��
#  0 : �P��񓚁i���W�I�{�^���j
#  1 : �����񓚁i�`�F�b�N�{�b�N�X�j
$type = 0;

# �W�v���ʂ̓\�[�g����
#  0 : ���Ȃ�
#  1 : ����
$sort = 1;

# ���e�����i�Z�L�����e�B�΍�j
#  0 : ���Ȃ�
#  1 : ����IP�A�h���X����̓��e�Ԋu�𐧌�����
#  2 : �S�Ă̓��e�Ԋu�𐧌�����
$regCtl = 1;

# �������e�Ԋu�i�b���j
#  �� $regCtl �ł̓��e�Ԋu
$wait = 10;

# ���e���́umethod=POST�v���� (0=no 1=yes)
#  �� �Z�L�����e�B�΍�
$postonly = 1;

# ���T�C�g���瓊�e�r�����Ɏw�肷��ꍇ�i�Z�L�����e�B�΍�j
#  �� �f����URL��http://���珑��
$baseUrl = '';

# �T�u�^�C�g��
#  �� �^�C�g�����ɃT�u�^�C�g�����L�q���܂��B�i�^�O�g�p�j
$subtitle = <<'EOM';
<!-- �������� -->
<p style="text-align: center;">
�M�������̎�ɏ������Ă��鐴��Ƃ��钘���i�P�s�{�j�Ƀ`�F�b�N�����Ȃ��`���I�I�I<br>
�i�A���񓚂�5�b���炢�҂��Ăˁj
</p>
<!-- �����܂� -->
EOM

# �^�C�g���摜���g���ꍇ (http://����摜���w��)
$ImgT = "";

# �^�C�g���摜���g���ꍇ�Ɂu�����v�u�c���v�����ꂼ��s�N�Z�����ŋL�q
$ImgW = 300;
$ImgH = 70;

# �^�O�L���}���I�v�V����
#  �� <!-- �㕔 --> <!-- ���� --> �̑���Ɂu�L���^�O�v��}���B
#  �� �L���^�O�ȊO�ɁAMIDI�^�O��LimeCounter���̃^�O�ɂ��g�p�B
$banner1 = '<!-- �㕔 -->';  # �㕔�ɑ}��
$banner2 = '<!-- ���� -->';  # �����ɑ}��

# �z�X�g�擾���@
# 0 : gethostbyaddr�֐����g��Ȃ�
# 1 : gethostbyaddr�֐����g��
$gethostbyaddr = 0;

#-------------------------------------------------
#  ���ݒ芮��
#-------------------------------------------------

# ���C������
&decode;
if ($mode eq 'regist') { &regist; }
elsif ($mode eq 'admin') { &admin; }
elsif ($mode eq 'item' && $freeitem) { &item; }
elsif ($mode eq 'check') { &check; }
&html;

#------------#
#  �������  #
#------------#
sub html {
	local($top,$num,$all,$all2,$ip,$tim,$no,$item,$count,$i,$r,$bef,$per,@type);

	# �f�[�^�ǂݍ���
	open(IN,"$logfile") || &error("Open Error: $logfile");
	$top = <IN>;
	($num,$all,$ip,$tim) = split(/<>/, $top);

	# ���v���R���}�t��
	$all2 = &filler($all);

	# ��ʏo��
	&header;
	print <<EOM;
<form>
<input type=button value="�g�b�v�ɖ߂�" onClick=window.open("$home","_top")>
</form>
<div align="center">
EOM

	# �C�Ӄ^�O
	print "$banner1<p>\n" if ($banner1 ne "<!-- �㕔 -->");

	# �^�C�g��
	if ($ImgT) {
		print "<img src=\"$ImgT\" width=$ImgW height=$ImgH alt=\"$title\">\n";
	} else {
		print "<b style=\"font-size:$t_size;color:$t_color\">$title</b>\n";
	}

	print <<EOM;
<p><table>
<tr><td>$subtitle</td></tr>
</table>
<p>�m�S���[���@<b>$all2</b>�[�n</p>
<form action="$script" method="POST">
<input type=hidden name=mode value="regist">
<table border=1 cellpadding=3 cellspacing=0>
<tr>
  <th class=l nowrap>��</th>
EOM

	if ($sort) { print "<th class=l nowrap>����</th>"; }

	print <<EOM;
  <th class=l nowrap>����</th>
  <th class=l nowrap>���[</th>
  <th class=l nowrap>����</th>
</tr>
EOM

	# �񓚃t�H�[�����`
	@type = ('radio', 'checkbox');

	$i=0;
	$r=1;
	while (<IN>) {
		$i++;
		($no,$item,$count) = split(/<>/);

		if ($all > 0) {
			$per = sprintf("%.1f", $count*100/$all);
			if ($per > 100) { $per = 100; }
			$wid = int($per * 5);
		} else {
			$per = 0.0;
			$wid = 1;
		}
		$count = &filler($count);
		if ($count ne $bef) { $r = $i; }

		print "<tr><th class=r>
		<input type=\"$type[$type]\" name=no value=\"$no\"></th>";

		if ($sort) { print "<th class=r>$r</th>"; }

		print "<td class=r><b>$item</b></td>
		<td class=r align=right>$count</td>
		<td class=r><img src=\"$graph\" height=\"10\" width=\"$wid\" alt=\"$per\">
		$per\%</td></tr>\n";

		$bef = $count;
	}
	close(IN);

	print <<EOM;
</table>
<p>
<input type=submit value="�񓚂���">
<input type=reset value="��߂Ƃ�">
</form>
<br><br>
EOM

	# ���ڒǉ�
	if ($freeitem) {
		print "<table><tr><td>\n";
		print "�����ڂ�ǉ�����ꍇ<br>\n";
		print "<form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=mode value=\"item\">\n";
		print "<input type=text name=item size=32>\n";
		print "<input type=submit value='�ǉ�'></form>\n";
		print "</td></tr></table>\n";
	}

	# �Ǘ��p�t�H�[��
	print <<EOM;
<div align=right>
<form action="$script" method="POST">
<input type=hidden name=mode value="admin">
<input type=password name=pass size=6>
<input type=submit value='Admin'></form></div>
<!-- ���쌠�\\��:�폜�s�� ($ver) -->
$banner2
<p>
<div align="center" style="font-size:10px;font-family:Verdana,Helvetica,Arial">
- <a href="http://www.kent-web.com/" target="_top">WebEnquete</a> -
</div>
</body>
</html>
EOM
	exit;
}

#------------#
#  ���[��t  #
#------------#
sub regist {
	local($time,$addr,$host,$top,$no,$item,$count,$hos,$ans,$vote,@ans,@new,@data,@sort);

	# �Z�L�����e�B�`�F�b�N
	if ($postonly && !$post_flag) {
		&error("�s���ȏ����̂��ߏ����𒆒f���܂���");
	}
	if ($baseUrl) {
		local($ref) = $ENV{'HTTP_REFERER'};
		$ref =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;
		$baseUrl =~ s/(\W)/\\$1/g;
		if ($ref && $ref !~ /$baseUrl/i) { &error("�s���ȃA�N�Z�X�ł�"); }
	}

	# �z�X�g�E���Ԃ��擾
	($addr, $host) = &get_host;
	$time = time;

	# ���[���
	if ($in{'no'} eq "") {
		return;
	} elsif ($type == 0) {
		if ($in{'no'} =~ /\0/) { &error("�����񓚂͂ł��܂���"); }
		$ans[0] = $in{'no'};
	} else {
		@ans = split(/\0/, $in{'no'});
	}

	# ���b�N�J�n
	&lock if ($lockkey);

	@data=();
	@sort=();
	open(IN,"$logfile") || &error("Open Error: $logfile");
	$top = <IN>;
	local($num,$al2,$ip,$tim) = split(/<>/, $top);

	$flag=0;
	if ($regCtl == 1) {
		if ($addr eq $ip && $time - $tim < $wait) { $flag=1; }
	} elsif ($regCtl == 2) {
		if ($time - $tim < $wait) { $flag=1; }
	}
	if ($flag) {
		&error("�Z�L�����e�B��A�Z���ԓ��̘A�����e�͐������Ă��܂��B���߂�Ȃ����B����������Ƒ҂��Ă���܂����肢���܂��B");
	}

	$all=0;
	while (<IN>) {
		($no,$item,$count,$hos) = split(/<>/);

		foreach $ans (@ans) {
			if ($no == $ans) {
				$count++;
				$_ = "$no<>$item<>$count<>$hos<>\n";
				$vote .= "$item ";
				last;
			}
		}
		push(@data,$_);
		push(@sort,$count);

		$all += $count;
	}
	close(IN);

	# �\�[�g����
	if ($sort) {
		@data = @data[sort {$sort[$b] <=> $sort[$a]} 0 .. $#sort];
	}

	# �X�V
	unshift(@data,"$num<>$all<>$addr<>$time<>\n");
	open(OUT,">$logfile") || &error("Write Error: $logfile");
	print OUT @data;
	close(OUT);

	# �A�N�Z�X���O
	&axslog('���[',$vote);

	# ���b�N����
	&unlock if ($lockkey);

	# �������b�Z�[�W
	&message("���񓚂��肪�Ƃ��������܂���");
}

#--------------#
#  �Ǘ����[�h  #
#--------------#
sub admin {
	local($top,$no,$al2,$ip,$tim,$all,$item,$count,$host,@data,@new);

	# �p�X���[�h�`�F�b�N
	if ($in{'pass'} ne $pass) { &error("�p�X���[�h���Ⴂ�܂�"); }

	# ���ڒǉ�����
	if ($in{'job'} eq "new" && $in{'item'} ne "") {

		# ���b�N�J�n
		&lock if ($lockkey);

		# ���O�Ǎ�
		open(IN,"$logfile") || &error("Open Error: $logfile");
		@data = <IN>;
		close(IN);
		$top = shift(@data);

		# ����No���̔�
		($no,$all,$ip,$tim) = split(/<>/, $top);
		$no++;

		# �X�V
		open(OUT,">$logfile") || &error("Write Error: $logfile");
		print OUT "$no<>$all<>$ip<>$tim<>\n";
		print OUT @data;
		print OUT "$no<>$in{'item'}<>0<><>\n";
		close(OUT);

		# ���b�N����
		&unlock if ($lockkey);

	# �C���t�H�[��
	} elsif ($in{'job'} eq 'edit' && $in{'no'}) {

		open(IN,"$logfile") || &error("Open Error: $logfile");
		$top = <IN>;
		while (<IN>) {
			($no,$item,$count,$host) = split(/<>/);
			last if ($in{'no'} == $no);
		}
		close(IN);

		&edit_form($no,$item,$count,$host);

	# �C�����s
	} elsif ($in{'job'} eq 'edit2') {

		# ���̓`�F�b�N
		if ($in{'item'} eq '') { &error('���ږ��ɓ��͂�����܂���'); }
		if ($in{'count'} =~ /\D/) {
			&error('���[���ɔ��p�����ȊO�̕��������͂���Ă��܂�');
		}

		# ���b�N�J�n
		&lock if ($lockkey);

		$all=0;
		@new=();
		open(IN,"$logfile") || &error("Open Error: $logfile");
		$top = <IN>;
		while (<IN>) {
			($no,$item,$count,$host) = split(/<>/);
			if ($in{'no'} == $no) {
				$_ = "$no<>$in{'item'}<>$in{'count'}<>$host<>\n";
				$count = $in{'count'};
			}
			push(@new,$_);

			$all += $count;
		}
		close(IN);

		($no,$al2,$ip,$tim) = split(/<>/, $top);

		# �X�V
		unshift(@new,"$no<>$all<>$ip<>$tim<>\n");
		open(OUT,">$logfile") || &error("Write Error: $logfile");
		print OUT @new;
		close(OUT);

		# ���b�N����
		&unlock if ($lockkey);

	# �폜����
	} elsif ($in{'job'} eq 'dele' && $in{'no'}) {

		# ���b�N�J�n
		&lock if ($lockkey);

		$all=0;
		@new=();
		open(IN,"$logfile") || &error("Open Error: $logfile");
		$top = <IN>;
		while (<IN>) {
			($no,$item,$count,$host) = split(/<>/);
			next if ($in{'no'} == $no);
			push(@new,$_);

			$all += $count;
		}
		close(IN);

		($no,$al2,$ip,$tim) = split(/<>/, $top);

		# �X�V
		open(OUT,">$logfile") || &error("Write Error: $logfile");
		print OUT "$no<>$all<>$ip<>$tim<>\n";
		print OUT @new;
		close(OUT);

		# ���b�N����
		&unlock if ($lockkey);

	# ���O�{��
	} elsif ($in{'job'} eq "log") {

		&axsView;

	# ���O�C��
	} else {

		# �z�X�g�擾
		($addr, $host) = &get_host;

		# �A�N�Z�X���O
		&axslog('�Ǘ����[�h','���O�C��');

	}

	# �Ǘ����
	&header;
	print <<"EOM";
<table><tr><td>
<form action="$script">
<input type=submit value="TOP��ʂ�"></td></form>
<td>
<form action="$script" method="POST">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=mode value="admin">
<input type=hidden name=job value="log">
<input type=submit value="�A�N�Z�X���O"></td></form>
</tr></table>
<hr>
<b>�����ڂ̒ǉ�</b>
<form action="$script" method="POST">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=mode value="admin">
<input type=hidden name=job value="new">
���ږ� <input type=text name=item size=30>
<input type=submit value="�ǉ�����">
</form>
<hr>
<b>�����ڃ����e�i���X</b>
<form action="$script" method="POST">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=mode value="admin">
���� <select name=job>
<option value="edit">�C��
<option value="dele">�폜
</select>
<input type=submit value="�I������">
<p>
<table border=1 cellspacing=0 cellpadding=3>
<tr>
  <th class=l>�I��</th>
  <th class=l>���ږ�</th>
  <th class=l>���[</th>
EOM
	print "<th class=l>���ڒǉ��z�X�g��</th>\n" if ($freeitem);
	print "</tr>\n";

	open(IN,"$logfile") || &error("Open Error: $logfile");
	$top = <IN>;
	while (<IN>) {
		($no,$item,$count,$host) = split(/<>/);
		print "<tr><th class=r><input type=radio name=no value=\"$no\"></th>";
		print "<td class=r><b>$item</b></td><td class=r align=right>$count</td>";
		if ($freeitem) {
			if (!$host) { $host = "<br>"; }
			print "<td class=r>$host</td>";
		}
		print "</tr>\n";
	}
	close(IN);

	print <<EOM;
</table>
</form>
</body>
</html>
EOM
	exit;
}

#------------#
#  �C�����  #
#------------#
sub edit_form {
	local($no,$item,$count,$host) = @_;

	&header;
	print <<EOM;
<form>
<input type=button value="�O��ʂɖ߂�" onClick="history.back()">
</form>
���C�����鍀�ڂ̂ݕύX���đ��M�{�^���������ĉ������B
<form action="$script" method="POST">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=mode value=admin>
<input type=hidden name=job value=edit2>
<input type=hidden name=no value="$in{'no'}">
���ږ�<br><input type=text name=item size=25 value="$item"><br>
���[��<br><input type=text name=count size=8 value="$count">
<p>
<input type=submit value="���M����">
</form>
</body>
</html>
EOM
	exit;
}

#------------#
#  ���ڒǉ�  #
#------------#
sub item {
	local($f,$top,$all,$ip,$tim,$no,$item,$count,$hos);

	# �t�H�[���`�F�b�N
	if ($in{'item'} eq "") { &error("���ږ��ɓ��͂�����܂���"); }

	# �z�X�g���`�F�b�N
	($addr, $host) = &get_host;

	# ���b�N�J�n
	&lock if ($lockkey);

	# ���O�Ǎ�
	$f=0;
	@data=();
	open(IN,"$logfile") || &error("Open Error: $logfile");
	$top = <IN>;
	while (<IN>) {
		($no,$item,$count,$hos) = split(/<>/);

		if ($in{'item'} eq $item) { $f++; last; }
		push(@data,$_);
	}
	close(IN);

	if ($f) {
		&error("���w��̍��ڂ͊��ɓo�^����Ă��܂�");
	} elsif ($freeitem == 1 && $host eq $hos) {
		&error("�A���������ڒǉ��͂ł��܂���");
	}

	# ����No���̔�
	($no,$all,$ip,$tim) = split(/<>/, $top);
	$no++;
	$all++;

	# �X�V
	open(OUT,">$logfile") || &error("Write Error: $logfile");
	print OUT "$no<>$all<>$addr<>$tim<>\n";
	print OUT @data;
	print OUT "$no<>$in{'item'}<>1<>$host<>\n";
	close(OUT);

	# �A�N�Z�X���O
	&axslog('���ڒǉ�',$in{'item'});

	# ���b�N����
	&unlock if ($lockkey);

	# �������b�Z�[�W
	&message("���ڂ�ǉ����܂���");
}

#------------#
#  ���O�L�^  #
#------------#
sub axslog {
	local($type,$vote) = @_;
	local($date,$agent,@data);

	$vote =~ s/\s$//;

	# ����
	local($sec,$min,$hour,$mday,$mon,$year) = localtime(time);
	$date = sprintf("%04d/%02d/%02d-%02d:%02d:%02d",
			$year+1900,$mon+1,$mday,$hour,$min,$sec);

	open(IN,"$axslog") || &error("Open Error: $axslog");
	@data = <IN>;
	close(IN);

	# �ێ�������
	while ($logMax <= @data) { pop(@data); }

	# �u���E�U���
	$agent = $ENV{'HTTP_USER_AGENT'};
	$agent =~ s/&/&amp;/g;
	$agent =~ s/</&lt;/g;
	$agent =~ s/>/&gt;/g;
	$agent =~ s/"/&quot;/g;

	open(OUT,">$axslog") || &error("Write Error: $axslog");
	print OUT "$date<>$type<>$vote<>$host<>$agent<>\n";
	print OUT @data;
	close(OUT);
}

#------------#
#  ���O�{��  #
#------------#
sub axsView {
	local($date,$type,$vote,$host,$agent);

	&header;
	print <<EOM;
<form>
<input type=button value="�O��ʂɖ߂�" onClick="history.back()">
</form>
<h3>�A�N�Z�X���O</h3>
<dl>
EOM

	# ���O�W�J
	open(IN,"$axslog") || &error("Open Error: $axslog");
	while (<IN>) {
		($date,$type,$vote,$host,$agent) = split(/<>/);

		print "<dt><hr>$date [$type] <b>$vote</b>
		<dd>[Host] $host<dd>[Agent] $agent\n";
	}
	close(IN);

	print <<EOM;
<dt><hr>
</dl>
</body>
</html>
EOM
	exit;
}

#----------------#
#  �f�R�[�h����  #
#----------------#
sub decode {
	local($buf, $key, $val);

	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		$post_flag=1;
		read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
	} else {
		$post_flag=0;
		$buf = $ENV{'QUERY_STRING'};
	}
	%in=();
	foreach ( split(/&/, $buf) ) {
		($key, $val) = split(/=/);
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;

		# S-JIS�R�[�h�ϊ�
		&jcode'convert(*val, 'sjis');

		# �^�O����
		$val =~ s/&/&amp;/g;
		$val =~ s/"/&quot;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;
		$val =~ s/\0//g;
		$val =~ s/\r//g;
		$val =~ s/\n//g;

		$in{$key} .= "\0" if (defined($in{$key}));
		$in{$key} .= $val;
	}
	$mode = $in{'mode'};

	# �^�C���]�[���ݒ�
	$ENV{'TZ'} = "JST-9";
}

#--------------#
#  HTML�w�b�_  #
#--------------#
sub header {
	print "Content-type: text/html\n\n";
	print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<META HTTP-EQUIV="Content-Style-Type" content="text/css">
<link rel="stylesheet" href="../../seino.css" type="text/css">
<STYLE type="text/css">
<!--
body,tr,td,th { font-size:$b_size; font-family:"$b_face"; }
a:link    { text-decoration:none; }
a:visited { text-decoration:none; }
a:active  { text-decoration:none; }
a:hover   { text-decoration:underline; color:red; }
.l { background-color: $tblCol2; color: $tblCol1; }
.r { background-color: $tblCol4; color: $tblCol3; }
-->
</STYLE>
<title>����Ƃ���A���P�[�g�@���̂P</title></head>
$body
EOM
	$headflag=1;
}

#--------------#
#  �G���[����  #
#--------------#
sub error {
	if ($lockflag) { rmdir($lockfile); }

	&header if (!$headflag);
	print <<EOM;
<div align="center">
<hr width=400><h3>ERROR !</h3>
<font color="#dd0000">$_[0]</font>
<p>
<hr width=400>
<p>
<form>
<input type=button value="�O��ʂɖ߂�" onClick="history.back()">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#--------------#
#  ���b�N����  #
#--------------#
sub lock {
	local($retry, $mtime);

	# �Â����b�N�͍폜
	if (-e $lockfile) {
		($mtime) = (stat($lockfile))[9];
		if ($mtime < time - 30) { &unlock; }
	}
	# ���b�N����
	$retry=5;
	while (!mkdir($lockfile, 0755)) {
		if (--$retry <= 0) { &error('LOCK is BUSY'); }
		sleep(1);
	}
	$lockflag=1;
}

#--------------#
#  ���b�N����  #
#--------------#
sub unlock {
	rmdir($lockfile);
	$lockflag=0;
}

#------------#
#  ����؂�  #
#------------#
sub filler {
	local($_) = $_[0];
	1 while s/(.*\d)(\d\d\d)/$1,$2/;
	$_;
}

#----------------#
#  �z�X�g���擾  #
#----------------#
sub get_host {
	local($host,$addr);

	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};

	if ($gethostbyaddr && ($host eq "" || $host eq $addr)) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
	}
	if ($host eq "") { $host = $addr; }

	return ($addr, $host);
}

#------------#
#  ��������  #
#------------#
sub message {
	local($msg) = @_;

	&header;
	print <<EOM;
<div align="center">
<hr width=400>
<h3>$msg</h3>
<hr width=400>
<p>
<form action="$script">
<input type=submit value="TOP�ɖ߂�">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#------------------#
#  �`�F�b�N���[�h  #
#------------------#
sub check {
	local($i,@file);

	&header;
	print <<EOM;
<h2>Check Mode</h2>
<UL>
EOM

	$i=0;
	@file = ('�f�[�^�t�@�C��','�A�N�Z�X���O');
	foreach ($logfile, $axslog) {

		# �p�X
		if (-e $_) {
			print "<LI>$file[$i]�F�p�XOK\n";

			if (-r $_ && -w $_) {
				print "<LI>$file[$i]�F�p�[�~�b�V����OK\n";
			} else {
				print "<LI>$file[$i]�F�p�[�~�b�V����NG\n";
			}
		} else {
			print "<LI>$file[$i]�F�p�XNG �� $_\n";
		}
		$i++;
	}

	# ���b�N�f�B���N�g��
	print "<LI>���b�N�`���F";
	if ($lockkey == 0) { print "���b�N�ݒ�Ȃ�\n"; }
	else {
		print "���b�N�ݒ肠��\n";

		($lockdir) = $lockfile =~ /(.*)[\\\/].*$/;
		print "<LI>���b�N�f�B���N�g���F$lockdir\n";

		if (-d $lockdir) { print "<LI>���b�N�f�B���N�g���̃p�X�FOK\n"; }
		else { print "<LI>���b�N�f�B���N�g���̃p�X�FNG �� $lockdir\n"; }

		if (-r $lockdir && -w $lockdir && -x $lockdir) {
			print "<LI>���b�N�f�B���N�g���̃p�[�~�b�V�����FOK\n";
		} else {
			print "<LI>���b�N�f�B���N�g���̃p�[�~�b�V�����FNG �� $lockdir\n";
		}
	}

	print <<EOM;
<LI>$ver
</UL>
</body>
</html>
EOM
	exit;
}

__END__

