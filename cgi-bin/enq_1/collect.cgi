#!/usr/local/bin/perl

#┌─────────────────────────────────
#│  WEB ENQUETE v4.2 (2004/01/02)
#│  Copyright (c) KentWeb
#│  webmaster@kent-web.com
#│  http://www.kent-web.com/
#└─────────────────────────────────
$ver = 'WEB ENQUETE v4.2';
#┌─────────────────────────────────
#│ [注意事項]
#│ 1. このスクリプトはフリーソフトです。このスクリプトを使用した
#│    いかなる損害に対して作者は一切の責任を負いません。
#│ 2. 設置に関する質問はサポート掲示板にお願いいたします。
#│    直接メールによる質問は一切お受けいたしておりません。
#└─────────────────────────────────
#
# 【ファイル構成例】
#
#  public_html (ホームディレクトリ)
#      |
#      +-- enq / enq.cgi    [705]
#           |    enq.log    [606]
#           |    axslog.cgi [606]
#           |    jcode.pl   [604]
#           |    graph.gif
#           |
#           +-- lock [707] /
#
# 【チェックモード呼び出し例】
#
#  http://www.xxx.xxx/enq/enq.cgi?mode=check
#

#-------------------------------------------------
#  ▼基本設定
#-------------------------------------------------

# ライブラリ取り込み
require './jcode.pl';

# タイトル名
$title = "清野とおるアンケート　その１<br>貴方の手にした単行本";

# タイトル文字の色
$t_color = "#444444";

# タイトル文字サイズ
$t_size = '20px';

# 本文の文字サイズ
$b_size = '13px';

# 本文の文字フォント
$b_face = "MS UI Gothic, Osaka";

# スクリプトURL
$script = './collect.cgi';

# データファイル
$logfile = './enq.log';

# アクセスログ
$axslog = './axslog.cgi';

# アクセスログの記録数
$logMax = 200;

# 管理用パスワード
$pass = 'azusawa3';

# ユーザ項目追加機能（ユーザが自由に項目を追加可能）
#  0 : しない
#  1 : する（同一IPによる連続した追加行為は禁止）
#  2 : する（同一IPによる連続した追加行為は可能）
$freeitem = 0;

# グラフ画像 (絶対パスだと http://から)
$graph = "./graph.gif";

# 戻り先 (絶対パスだと http://から)
$home = "../../index.html";

# bodyタグ
$body = '<body bgcolor="#ffffff" text="#111111">';

# テーブル内「タイトル」セル色
$tblCol1 = "#111111";	# 文字色
$tblCol2 = "#ffffff";	# 下地色

# テーブル内「項目」セル色
$tblCol3 = "#000000";	# 文字色
$tblCol4 = "#ccffdd";	# 下地色

# ロックファイル機構 (0=no 1=yes)
$lockkey = 0;

# ロックファイル名
$lockfile = './lock/enq.lock';

# 投票の回答形式
#  0 : 単一回答（ラジオボタン）
#  1 : 複数回答（チェックボックス）
$type = 0;

# 集計結果はソートする
#  0 : しない
#  1 : する
$sort = 1;

# 投稿制限（セキュリティ対策）
#  0 : しない
#  1 : 同一IPアドレスからの投稿間隔を制限する
#  2 : 全ての投稿間隔を制限する
$regCtl = 1;

# 制限投稿間隔（秒数）
#  → $regCtl での投稿間隔
$wait = 10;

# 投稿時は「method=POST」限定 (0=no 1=yes)
#  → セキュリティ対策
$postonly = 1;

# 他サイトから投稿排除時に指定する場合（セキュリティ対策）
#  → 掲示板のURLをhttp://から書く
$baseUrl = '';

# サブタイトル
#  → タイトル下にサブタイトルを記述します。（タグ使用可）
$subtitle = <<'EOM';
<!-- ここから -->
<p style="text-align: center;">
貴方が其の手に所持している清野とおる著書（単行本）にチェックを入れなさ～い！！！<br>
（連続回答は5秒くらい待ってね）
</p>
<!-- ここまで -->
EOM

# タイトル画像を使う場合 (http://から画像を指定)
$ImgT = "";

# タイトル画像を使う場合に「横幅」「縦幅」をそれぞれピクセル数で記述
$ImgW = 300;
$ImgH = 70;

# タグ広告挿入オプション
#  → <!-- 上部 --> <!-- 下部 --> の代わりに「広告タグ」を挿入。
#  → 広告タグ以外に、MIDIタグやLimeCounter等のタグにも使用可。
$banner1 = '<!-- 上部 -->';  # 上部に挿入
$banner2 = '<!-- 下部 -->';  # 下部に挿入

# ホスト取得方法
# 0 : gethostbyaddr関数を使わない
# 1 : gethostbyaddr関数を使う
$gethostbyaddr = 0;

#-------------------------------------------------
#  ▲設定完了
#-------------------------------------------------

# メイン処理
&decode;
if ($mode eq 'regist') { &regist; }
elsif ($mode eq 'admin') { &admin; }
elsif ($mode eq 'item' && $freeitem) { &item; }
elsif ($mode eq 'check') { &check; }
&html;

#------------#
#  初期画面  #
#------------#
sub html {
	local($top,$num,$all,$all2,$ip,$tim,$no,$item,$count,$i,$r,$bef,$per,@type);

	# データ読み込み
	open(IN,"$logfile") || &error("Open Error: $logfile");
	$top = <IN>;
	($num,$all,$ip,$tim) = split(/<>/, $top);

	# 総計をコンマ付加
	$all2 = &filler($all);

	# 画面出力
	&header;
	print <<EOM;
<form>
<input type=button value="トップに戻る" onClick=window.open("$home","_top")>
</form>
<div align="center">
EOM

	# 任意タグ
	print "$banner1<p>\n" if ($banner1 ne "<!-- 上部 -->");

	# タイトル
	if ($ImgT) {
		print "<img src=\"$ImgT\" width=$ImgW height=$ImgH alt=\"$title\">\n";
	} else {
		print "<b style=\"font-size:$t_size;color:$t_color\">$title</b>\n";
	}

	print <<EOM;
<p><table>
<tr><td>$subtitle</td></tr>
</table>
<p>［全投票数　<b>$all2</b>票］</p>
<form action="$script" method="POST">
<input type=hidden name=mode value="regist">
<table border=1 cellpadding=3 cellspacing=0>
<tr>
  <th class=l nowrap>回答</th>
EOM

	if ($sort) { print "<th class=l nowrap>順位</th>"; }

	print <<EOM;
  <th class=l nowrap>項目</th>
  <th class=l nowrap>得票</th>
  <th class=l nowrap>割合</th>
</tr>
EOM

	# 回答フォームを定義
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
<input type=submit value="回答する">
<input type=reset value="やめとく">
</form>
<br><br>
EOM

	# 項目追加
	if ($freeitem) {
		print "<table><tr><td>\n";
		print "▽項目を追加する場合<br>\n";
		print "<form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=mode value=\"item\">\n";
		print "<input type=text name=item size=32>\n";
		print "<input type=submit value='追加'></form>\n";
		print "</td></tr></table>\n";
	}

	# 管理用フォーム
	print <<EOM;
<div align=right>
<form action="$script" method="POST">
<input type=hidden name=mode value="admin">
<input type=password name=pass size=6>
<input type=submit value='Admin'></form></div>
<!-- 著作権表\示:削除不可 ($ver) -->
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
#  投票受付  #
#------------#
sub regist {
	local($time,$addr,$host,$top,$no,$item,$count,$hos,$ans,$vote,@ans,@new,@data,@sort);

	# セキュリティチェック
	if ($postonly && !$post_flag) {
		&error("不正な処理のため処理を中断しました");
	}
	if ($baseUrl) {
		local($ref) = $ENV{'HTTP_REFERER'};
		$ref =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;
		$baseUrl =~ s/(\W)/\\$1/g;
		if ($ref && $ref !~ /$baseUrl/i) { &error("不正なアクセスです"); }
	}

	# ホスト・時間を取得
	($addr, $host) = &get_host;
	$time = time;

	# 投票情報
	if ($in{'no'} eq "") {
		return;
	} elsif ($type == 0) {
		if ($in{'no'} =~ /\0/) { &error("複数回答はできません"); }
		$ans[0] = $in{'no'};
	} else {
		@ans = split(/\0/, $in{'no'});
	}

	# ロック開始
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
		&error("セキュリティ上、短時間内の連続投稿は制限しています。ごめんなさい。もうちょっと待ってからまたお願いします。");
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

	# ソート処理
	if ($sort) {
		@data = @data[sort {$sort[$b] <=> $sort[$a]} 0 .. $#sort];
	}

	# 更新
	unshift(@data,"$num<>$all<>$addr<>$time<>\n");
	open(OUT,">$logfile") || &error("Write Error: $logfile");
	print OUT @data;
	close(OUT);

	# アクセスログ
	&axslog('投票',$vote);

	# ロック解除
	&unlock if ($lockkey);

	# 完了メッセージ
	&message("ご回答ありがとうございました");
}

#--------------#
#  管理モード  #
#--------------#
sub admin {
	local($top,$no,$al2,$ip,$tim,$all,$item,$count,$host,@data,@new);

	# パスワードチェック
	if ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	# 項目追加処理
	if ($in{'job'} eq "new" && $in{'item'} ne "") {

		# ロック開始
		&lock if ($lockkey);

		# ログ読込
		open(IN,"$logfile") || &error("Open Error: $logfile");
		@data = <IN>;
		close(IN);
		$top = shift(@data);

		# 項目Noを採番
		($no,$all,$ip,$tim) = split(/<>/, $top);
		$no++;

		# 更新
		open(OUT,">$logfile") || &error("Write Error: $logfile");
		print OUT "$no<>$all<>$ip<>$tim<>\n";
		print OUT @data;
		print OUT "$no<>$in{'item'}<>0<><>\n";
		close(OUT);

		# ロック解除
		&unlock if ($lockkey);

	# 修正フォーム
	} elsif ($in{'job'} eq 'edit' && $in{'no'}) {

		open(IN,"$logfile") || &error("Open Error: $logfile");
		$top = <IN>;
		while (<IN>) {
			($no,$item,$count,$host) = split(/<>/);
			last if ($in{'no'} == $no);
		}
		close(IN);

		&edit_form($no,$item,$count,$host);

	# 修正実行
	} elsif ($in{'job'} eq 'edit2') {

		# 入力チェック
		if ($in{'item'} eq '') { &error('項目名に入力がありません'); }
		if ($in{'count'} =~ /\D/) {
			&error('投票数に半角数字以外の文字が入力されています');
		}

		# ロック開始
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

		# 更新
		unshift(@new,"$no<>$all<>$ip<>$tim<>\n");
		open(OUT,">$logfile") || &error("Write Error: $logfile");
		print OUT @new;
		close(OUT);

		# ロック解除
		&unlock if ($lockkey);

	# 削除処理
	} elsif ($in{'job'} eq 'dele' && $in{'no'}) {

		# ロック開始
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

		# 更新
		open(OUT,">$logfile") || &error("Write Error: $logfile");
		print OUT "$no<>$all<>$ip<>$tim<>\n";
		print OUT @new;
		close(OUT);

		# ロック解除
		&unlock if ($lockkey);

	# ログ閲覧
	} elsif ($in{'job'} eq "log") {

		&axsView;

	# ログイン
	} else {

		# ホスト取得
		($addr, $host) = &get_host;

		# アクセスログ
		&axslog('管理モード','ログイン');

	}

	# 管理画面
	&header;
	print <<"EOM";
<table><tr><td>
<form action="$script">
<input type=submit value="TOP画面へ"></td></form>
<td>
<form action="$script" method="POST">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=mode value="admin">
<input type=hidden name=job value="log">
<input type=submit value="アクセスログ"></td></form>
</tr></table>
<hr>
<b>▽項目の追加</b>
<form action="$script" method="POST">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=mode value="admin">
<input type=hidden name=job value="new">
項目名 <input type=text name=item size=30>
<input type=submit value="追加する">
</form>
<hr>
<b>▽項目メンテナンス</b>
<form action="$script" method="POST">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=mode value="admin">
処理 <select name=job>
<option value="edit">修正
<option value="dele">削除
</select>
<input type=submit value="選択する">
<p>
<table border=1 cellspacing=0 cellpadding=3>
<tr>
  <th class=l>選択</th>
  <th class=l>項目名</th>
  <th class=l>得票</th>
EOM
	print "<th class=l>項目追加ホスト名</th>\n" if ($freeitem);
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
#  修正画面  #
#------------#
sub edit_form {
	local($no,$item,$count,$host) = @_;

	&header;
	print <<EOM;
<form>
<input type=button value="前画面に戻る" onClick="history.back()">
</form>
▽修正する項目のみ変更して送信ボタンを押して下さい。
<form action="$script" method="POST">
<input type=hidden name=pass value="$in{'pass'}">
<input type=hidden name=mode value=admin>
<input type=hidden name=job value=edit2>
<input type=hidden name=no value="$in{'no'}">
項目名<br><input type=text name=item size=25 value="$item"><br>
投票数<br><input type=text name=count size=8 value="$count">
<p>
<input type=submit value="送信する">
</form>
</body>
</html>
EOM
	exit;
}

#------------#
#  項目追加  #
#------------#
sub item {
	local($f,$top,$all,$ip,$tim,$no,$item,$count,$hos);

	# フォームチェック
	if ($in{'item'} eq "") { &error("項目名に入力がありません"); }

	# ホスト名チェック
	($addr, $host) = &get_host;

	# ロック開始
	&lock if ($lockkey);

	# ログ読込
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
		&error("ご指定の項目は既に登録されています");
	} elsif ($freeitem == 1 && $host eq $hos) {
		&error("連続した項目追加はできません");
	}

	# 項目Noを採番
	($no,$all,$ip,$tim) = split(/<>/, $top);
	$no++;
	$all++;

	# 更新
	open(OUT,">$logfile") || &error("Write Error: $logfile");
	print OUT "$no<>$all<>$addr<>$tim<>\n";
	print OUT @data;
	print OUT "$no<>$in{'item'}<>1<>$host<>\n";
	close(OUT);

	# アクセスログ
	&axslog('項目追加',$in{'item'});

	# ロック解除
	&unlock if ($lockkey);

	# 完了メッセージ
	&message("項目を追加しました");
}

#------------#
#  ログ記録  #
#------------#
sub axslog {
	local($type,$vote) = @_;
	local($date,$agent,@data);

	$vote =~ s/\s$//;

	# 時間
	local($sec,$min,$hour,$mday,$mon,$year) = localtime(time);
	$date = sprintf("%04d/%02d/%02d-%02d:%02d:%02d",
			$year+1900,$mon+1,$mday,$hour,$min,$sec);

	open(IN,"$axslog") || &error("Open Error: $axslog");
	@data = <IN>;
	close(IN);

	# 保持数調整
	while ($logMax <= @data) { pop(@data); }

	# ブラウザ情報
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
#  ログ閲覧  #
#------------#
sub axsView {
	local($date,$type,$vote,$host,$agent);

	&header;
	print <<EOM;
<form>
<input type=button value="前画面に戻る" onClick="history.back()">
</form>
<h3>アクセスログ</h3>
<dl>
EOM

	# ログ展開
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
#  デコード処理  #
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

		# S-JISコード変換
		&jcode'convert(*val, 'sjis');

		# タグ処理
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

	# タイムゾーン設定
	$ENV{'TZ'} = "JST-9";
}

#--------------#
#  HTMLヘッダ  #
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
<title>清野とおるアンケート　その１</title></head>
$body
EOM
	$headflag=1;
}

#--------------#
#  エラー処理  #
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
<input type=button value="前画面に戻る" onClick="history.back()">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#--------------#
#  ロック処理  #
#--------------#
sub lock {
	local($retry, $mtime);

	# 古いロックは削除
	if (-e $lockfile) {
		($mtime) = (stat($lockfile))[9];
		if ($mtime < time - 30) { &unlock; }
	}
	# ロック処理
	$retry=5;
	while (!mkdir($lockfile, 0755)) {
		if (--$retry <= 0) { &error('LOCK is BUSY'); }
		sleep(1);
	}
	$lockflag=1;
}

#--------------#
#  ロック解除  #
#--------------#
sub unlock {
	rmdir($lockfile);
	$lockflag=0;
}

#------------#
#  桁区切り  #
#------------#
sub filler {
	local($_) = $_[0];
	1 while s/(.*\d)(\d\d\d)/$1,$2/;
	$_;
}

#----------------#
#  ホスト名取得  #
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
#  完了文言  #
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
<input type=submit value="TOPに戻る">
</form>
</div>
</body>
</html>
EOM
	exit;
}

#------------------#
#  チェックモード  #
#------------------#
sub check {
	local($i,@file);

	&header;
	print <<EOM;
<h2>Check Mode</h2>
<UL>
EOM

	$i=0;
	@file = ('データファイル','アクセスログ');
	foreach ($logfile, $axslog) {

		# パス
		if (-e $_) {
			print "<LI>$file[$i]：パスOK\n";

			if (-r $_ && -w $_) {
				print "<LI>$file[$i]：パーミッションOK\n";
			} else {
				print "<LI>$file[$i]：パーミッションNG\n";
			}
		} else {
			print "<LI>$file[$i]：パスNG → $_\n";
		}
		$i++;
	}

	# ロックディレクトリ
	print "<LI>ロック形式：";
	if ($lockkey == 0) { print "ロック設定なし\n"; }
	else {
		print "ロック設定あり\n";

		($lockdir) = $lockfile =~ /(.*)[\\\/].*$/;
		print "<LI>ロックディレクトリ：$lockdir\n";

		if (-d $lockdir) { print "<LI>ロックディレクトリのパス：OK\n"; }
		else { print "<LI>ロックディレクトリのパス：NG → $lockdir\n"; }

		if (-r $lockdir && -w $lockdir && -x $lockdir) {
			print "<LI>ロックディレクトリのパーミッション：OK\n";
		} else {
			print "<LI>ロックディレクトリのパーミッション：NG → $lockdir\n";
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

