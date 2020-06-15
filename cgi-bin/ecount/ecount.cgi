#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� e-Counter v1.3 (2001/08/25)
#�� Copyright(C) Kent Web 2001
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������
$ver = 'e-Counter v1.3';
#��������������������������������������������������������������������
#�� [���ӎ���]
#�� 1. ���̃X�N���v�g�̓t���[�\�t�g�ł��B���̃X�N���v�g���g�p����
#��    �����Ȃ鑹�Q�ɑ΂��č�҂͈�؂̐ӔC�𕉂��܂���B
#�� 2. �ݒu�Ɋւ��鎿��̓T�|�[�g�f���ɂ��肢�������܂��B
#��    ���ڃ��[���ɂ�鎿��͈�؂��󂯂������Ă���܂���B
#��������������������������������������������������������������������
#
# �y�f�B���N�g���^�t�@�C���\����z�������������̓p�[�~�b�V�����l
#
#  public_html / index.html (�g�b�v�y�[�W)
#       |
#       +-- cgi-bin / ecount.cgi [755]
#              |      ecount.dat [666]
#              |
#              +-- gif / 0.gif 1.gif .... 9.gif
#              |
#              +-- lock [777] /
#
# �y�^�O�̏������z
#  (1) IMG�^�O���u�����v�������L�q����
#  (2) �E�̃^�O���獶�̃^�O�֏��ɁA�����𐔎��i�����j�ŋL�q����
#
#   ��1 �F 4���ŕ\���������Ƃ�
#  <img src="cgi-bin/ecount.cgi?4">
#  <img src="cgi-bin/ecount.cgi?3">
#  <img src="cgi-bin/ecount.cgi?2">
#  <img src="cgi-bin/ecount.cgi?1">
#
#   ��2 �F 6���ŕ\���������Ƃ�
#  <img src="cgi-bin/ecount.cgi?6">
#  <img src="cgi-bin/ecount.cgi?5">
#  <img src="cgi-bin/ecount.cgi?4">
#  <img src="cgi-bin/ecount.cgi?3">
#  <img src="cgi-bin/ecount.cgi?2">
#  <img src="cgi-bin/ecount.cgi?1">
#
#  ����͌��₷���悤�Ƀ^�O���ɉ��s���Ă��܂����A���ۂ͉��s������
#    �S�Ẵ^�O����s�ŋL�q���܂��B
#
# �y�`�F�b�N���[�h�z
#  �E�����Ɂucheck�v��t���ČĂяo���ƊȈՓI�Ȑݒ�`�F�b�N���s�Ȃ��܂�
#
#  ��Fhttp://www.xxx.zzz/cgi-bin/ecount.cgi?check

#============#
#  �ݒ荀��  #
#============#

# ���O�t�@�C��
$logfile = './ecount.dat';

# �摜�`��
# G : GIF  (�摜�g���q�́u.gif�v�Ƃ��邱��)
# J : JPEG (�摜�g���q�́u.jpg�v�Ƃ��邱��)
# P : PNG  (�摜�g���q�́u.png�v�Ƃ��邱��)
$imgtype = 'G';

# �摜�f�B���N�g���i�Ō�� / �ŏI��邱�Ɓj
# �� �t���p�X���� / ����n�܂�p�X�ihttp://����ł͂Ȃ��j
$imgdir = './gif/';

# ���b�N�t�@�C���`��
# 0=no 1=symlink 2=mkdir
$lockkey = 2;

# ���b�N�t�@�C����
$lockfile = './lock/ecount.lock';

# IP�`�F�b�N�@�\�i�d���J�E���g�΍�j
# 0=no 1=yes
$ipcheck = 1;

#============#
#  �ݒ芮��  #
#============#

# �������擾���A�]�v�ȃR�[�h���폜
$buf = $ENV{'QUERY_STRING'};
$buf =~ s/\W//g;

# �������Ȃ��ꍇ�̓G���[
if ($buf eq "") { &error; }

# �摜�̊g���q��MIME�w�b�_���`
if ($imgtype eq 'J') { $tail='.jpg'; $mime='jpeg'; }
elsif ($imgtype eq 'P') { $tail='.png'; $mime='x-png'; }
else { $tail='.gif'; $mime='gif'; }

# �`�F�b�N���[�h�̂Ƃ��̓`�F�b�N����
if ($buf eq "check") { &check; }

# ���b�N�J�n
$lockflag=0;
if ($lockkey && $buf == 1) { $lockflag=1; &lock; }

# ���O��ǂݍ���ŕ���
open(IN,"$logfile") || &error;
$count = <IN>;
close(IN);
($count, $ip) = split(/:/, $count);

# �J�E���g�����P�������ɕ������ĕ\���摜���`
@file = split(//, $count);
if ($#file + 1 >= $buf) { $view = $file[$#file + 1 - $buf]; }
else { $view = '0'; }

# �摜��ǂݍ���ŕ\��
open(IMG,"$imgdir$view$tail") || &error;
print "Content-type: image\/$mime\n\n";
binmode(IMG);
binmode(STDOUT);
print <IMG>;
close(IMG);

# IP�`�F�b�N
$flag=0;
$addr = $ENV{'REMOTE_ADDR'};
if (($ipcheck && $addr ne $ip) || (!$ipcheck)) { $flag=1; $count++; }

# ���O�X�V���[�h
if ($buf == 1 && $flag == 1) {
	select(undef, undef, undef, 0.5);
	open(OUT,">$logfile") || &error;
	print OUT "$count\:$addr";
	close(OUT);
}

# ���b�N����
if ($lockflag) { &unlock; }

exit;


#--------------#
#  ���b�N����  #
#--------------#
sub lock {
	local($retry) = 5;
	# 1���ȏ�Â����b�N�͍폜����
	if (-e $lockfile) {
		local($mtime) = (stat($lockfile))[9];
		if ($mtime < time - 60) { &unlock; }
	}
	# symlink�֐������b�N
	if ($lockkey == 1) {
		while (!symlink(".", $lockfile)) {
			if (--$retry <= 0) { &error; }
			sleep(1);
		}
	# mkdir�֐������b�N
	} elsif ($lockkey == 2) {
		while (!mkdir($lockfile, 0755)) {
			if (--$retry <= 0) { &error; }
			sleep(1);
		}
	}
}

#--------------#
#  ���b�N����  #
#--------------#
sub unlock {
	if ($lockkey == 1) { unlink($lockfile); }
	elsif ($lockkey == 2) { rmdir($lockfile); }
}

#--------------#
#  �G���[����  #
#--------------#
sub error {
	if ($lockflag) { &unlock; }

	@err = ('47','49','46','38','39','61','2d','00','0f','00','80','00','00','00','00','00','ff','ff','ff','2c', '00','00','00','00','2d','00','0f','00','00','02','49','8c','8f','a9','cb','ed','0f','a3','9c','34', '81','7b','03','ce','7a','23','7c','6c','00','c4','19','5c','76','8e','dd','ca','96','8c','9b','b6', '63','89','aa','ee','22','ca','3a','3d','db','6a','03','f3','74','40','ac','55','ee','11','dc','f9', '42','bd','22','f0','a7','34','2d','63','4e','9c','87','c7','93','fe','b2','95','ae','f7','0b','0e', '8b','c7','de','02','00','3b');

	print "Content-type: image/gif\n\n";
	foreach (@err) {
		$data = pack('C*',hex($_));
		print $data;
	}
	exit;
}

#----------------#
#  �`�F�b�N�@�\  #
#----------------#
sub check {
	print "Content-type: text/html\n\n";
	print "<html><head><title>$ver</title></head>\n";
	print "<body>\n<h2>Check Mode</h2>\n<UL>\n";

	# ���O�̃p�X
	if (-e $logfile) { print "<LI>���O�t�@�C���̃p�X�FOK!\n"; }
	else { print "<LI>���O�t�@�C���̃p�X���s���ł��F$logfile\n"; }

	# �p�[�~�b�V����
	if (-r $logfile && -w $logfile) {
		print "<LI>���O�t�@�C���̃p�[�~�b�V�����FOK!\n";
	} else {
		print "<LI>���O�t�@�C���̃p�[�~�b�V�������s���ł�\n";
	}

	# �摜�t�@�C��
	foreach (0 .. 9) {
		if (-e "$imgdir$_$tail") {
			print "<LI>�摜�F$imgdir$_$tail �� OK! \n";
		} else {
			print "<LI>�摜�F$imgdir$_$tail �� NG! \n";
		}
	}

	# ���b�N�f�B���N�g��
	print "<LI>���b�N�`���F";
	if ($lockkey == 1) { print "symlink\n"; }
	elsif ($lockkey == 2) { print "mkdir\n"; }
	else { print "�Ȃ�\n"; }

	if ($lockkey) {
		($lockdir) = $lockfile =~ /(.*)[\\\/].*$/;
		if (-d $lockdir) { print "<LI>���b�N�f�B���N�g���̃p�X�FOK! \n"; }
		else { print "<LI>���b�N�f�B���N�g�����s���ł� �� $lockdir\n"; }

		if (-r $lockdir && -w $lockdir && -x $lockdir) {
			print "<LI>���b�N�f�B���N�g���̃p�[�~�b�V�����FOK! \n";
		} else {
			print "<LI>���b�N�f�B���N�g���̃p�[�~�b�V�������s���ł� �� $lockdir\n";
		}
	}

	# ���쌠�\���i�폜�E���ϕs�j
	print "<P><!-- $ver --><small>\n";
	print "- <a href='http://www.kent-web.com/'>$ver</a> -\n";
	print "</small></UL>\n</body>\n</html>\n";
	exit;
}
