#!/usr/local/bin/perl

#┌─────────────────────────────────
#│ e-Counter v1.3 (2001/08/25)
#│ Copyright(C) Kent Web 2001
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────
$ver = 'e-Counter v1.3';
#┌─────────────────────────────────
#│ [注意事項]
#│ 1. このスクリプトはフリーソフトです。このスクリプトを使用した
#│    いかなる損害に対して作者は一切の責任を負いません。
#│ 2. 設置に関する質問はサポート掲示板にお願いいたします。
#│    直接メールによる質問は一切お受けいたしておりません。
#└─────────────────────────────────
#
# 【ディレクトリ／ファイル構成例】かぎかっこ内はパーミッション値
#
#  public_html / index.html (トップページ)
#       |
#       +-- cgi-bin / ecount.cgi [755]
#              |      ecount.dat [666]
#              |
#              +-- gif / 0.gif 1.gif .... 9.gif
#              |
#              +-- lock [777] /
#
# 【タグの書き方】
#  (1) IMGタグを「桁数」分だけ記述する
#  (2) 右のタグから左のタグへ順に、引数を数字（桁数）で記述する
#
#   例1 ： 4桁で表示したいとき
#  <img src="cgi-bin/ecount.cgi?4">
#  <img src="cgi-bin/ecount.cgi?3">
#  <img src="cgi-bin/ecount.cgi?2">
#  <img src="cgi-bin/ecount.cgi?1">
#
#   例2 ： 6桁で表示したいとき
#  <img src="cgi-bin/ecount.cgi?6">
#  <img src="cgi-bin/ecount.cgi?5">
#  <img src="cgi-bin/ecount.cgi?4">
#  <img src="cgi-bin/ecount.cgi?3">
#  <img src="cgi-bin/ecount.cgi?2">
#  <img src="cgi-bin/ecount.cgi?1">
#
#  ↑例は見やすいようにタグ毎に改行していますが、実際は改行せずに
#    全てのタグを一行で記述します。
#
# 【チェックモード】
#  ・引数に「check」を付けて呼び出すと簡易的な設定チェックを行ないます
#
#  例：http://www.xxx.zzz/cgi-bin/ecount.cgi?check

#============#
#  設定項目  #
#============#

# ログファイル
$logfile = './ecount.dat';

# 画像形式
# G : GIF  (画像拡張子は「.gif」とすること)
# J : JPEG (画像拡張子は「.jpg」とすること)
# P : PNG  (画像拡張子は「.png」とすること)
$imgtype = 'G';

# 画像ディレクトリ（最後は / で終わること）
# → フルパスだと / から始まるパス（http://からではない）
$imgdir = './gif/';

# ロックファイル形式
# 0=no 1=symlink 2=mkdir
$lockkey = 2;

# ロックファイル名
$lockfile = './lock/ecount.lock';

# IPチェック機能（重複カウント対策）
# 0=no 1=yes
$ipcheck = 1;

#============#
#  設定完了  #
#============#

# 引数を取得し、余計なコードを削除
$buf = $ENV{'QUERY_STRING'};
$buf =~ s/\W//g;

# 引数がない場合はエラー
if ($buf eq "") { &error; }

# 画像の拡張子とMIMEヘッダを定義
if ($imgtype eq 'J') { $tail='.jpg'; $mime='jpeg'; }
elsif ($imgtype eq 'P') { $tail='.png'; $mime='x-png'; }
else { $tail='.gif'; $mime='gif'; }

# チェックモードのときはチェック処理
if ($buf eq "check") { &check; }

# ロック開始
$lockflag=0;
if ($lockkey && $buf == 1) { $lockflag=1; &lock; }

# ログを読み込んで分解
open(IN,"$logfile") || &error;
$count = <IN>;
close(IN);
($count, $ip) = split(/:/, $count);

# カウント数を１文字毎に分解して表示画像を定義
@file = split(//, $count);
if ($#file + 1 >= $buf) { $view = $file[$#file + 1 - $buf]; }
else { $view = '0'; }

# 画像を読み込んで表示
open(IMG,"$imgdir$view$tail") || &error;
print "Content-type: image\/$mime\n\n";
binmode(IMG);
binmode(STDOUT);
print <IMG>;
close(IMG);

# IPチェック
$flag=0;
$addr = $ENV{'REMOTE_ADDR'};
if (($ipcheck && $addr ne $ip) || (!$ipcheck)) { $flag=1; $count++; }

# ログ更新モード
if ($buf == 1 && $flag == 1) {
	select(undef, undef, undef, 0.5);
	open(OUT,">$logfile") || &error;
	print OUT "$count\:$addr";
	close(OUT);
}

# ロック解除
if ($lockflag) { &unlock; }

exit;


#--------------#
#  ロック処理  #
#--------------#
sub lock {
	local($retry) = 5;
	# 1分以上古いロックは削除する
	if (-e $lockfile) {
		local($mtime) = (stat($lockfile))[9];
		if ($mtime < time - 60) { &unlock; }
	}
	# symlink関数式ロック
	if ($lockkey == 1) {
		while (!symlink(".", $lockfile)) {
			if (--$retry <= 0) { &error; }
			sleep(1);
		}
	# mkdir関数式ロック
	} elsif ($lockkey == 2) {
		while (!mkdir($lockfile, 0755)) {
			if (--$retry <= 0) { &error; }
			sleep(1);
		}
	}
}

#--------------#
#  ロック解除  #
#--------------#
sub unlock {
	if ($lockkey == 1) { unlink($lockfile); }
	elsif ($lockkey == 2) { rmdir($lockfile); }
}

#--------------#
#  エラー処理  #
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
#  チェック機構  #
#----------------#
sub check {
	print "Content-type: text/html\n\n";
	print "<html><head><title>$ver</title></head>\n";
	print "<body>\n<h2>Check Mode</h2>\n<UL>\n";

	# ログのパス
	if (-e $logfile) { print "<LI>ログファイルのパス：OK!\n"; }
	else { print "<LI>ログファイルのパスが不正です：$logfile\n"; }

	# パーミッション
	if (-r $logfile && -w $logfile) {
		print "<LI>ログファイルのパーミッション：OK!\n";
	} else {
		print "<LI>ログファイルのパーミッションが不正です\n";
	}

	# 画像ファイル
	foreach (0 .. 9) {
		if (-e "$imgdir$_$tail") {
			print "<LI>画像：$imgdir$_$tail → OK! \n";
		} else {
			print "<LI>画像：$imgdir$_$tail → NG! \n";
		}
	}

	# ロックディレクトリ
	print "<LI>ロック形式：";
	if ($lockkey == 1) { print "symlink\n"; }
	elsif ($lockkey == 2) { print "mkdir\n"; }
	else { print "なし\n"; }

	if ($lockkey) {
		($lockdir) = $lockfile =~ /(.*)[\\\/].*$/;
		if (-d $lockdir) { print "<LI>ロックディレクトリのパス：OK! \n"; }
		else { print "<LI>ロックディレクトリが不正です → $lockdir\n"; }

		if (-r $lockdir && -w $lockdir && -x $lockdir) {
			print "<LI>ロックディレクトリのパーミッション：OK! \n";
		} else {
			print "<LI>ロックディレクトリのパーミッションが不正です → $lockdir\n";
		}
	}

	# 著作権表示（削除・改変不可）
	print "<P><!-- $ver --><small>\n";
	print "- <a href='http://www.kent-web.com/'>$ver</a> -\n";
	print "</small></UL>\n</body>\n</html>\n";
	exit;
}
