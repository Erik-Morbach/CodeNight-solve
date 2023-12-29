#include <bits/stdc++.h>
using namespace std;
typedef long long int ll;
typedef pair<int,int> ii;
typedef vector<int> vi;
#define x first
#define y second
const int maxn = 10000 + 100;

ll v[maxn];

// Utiliza n² de memória. Não deveria passar, mas passava no contest
// n² ~= 1Gb
ll memo[maxn][maxn];
int vizi[maxn][maxn]; 
// Vizi define se uma celula da matriz foi vizitada
// Se vizi[i][j] == cnt; Você ja vizitou 
int cnt=1;

ll dp(int l, int r){
	if(vizi[l][r] == cnt) return memo[l][r];
	vizi[l][r] = cnt;
	int tam = r-l + 1;
	if(tam==2) return memo[l][r] = max(v[l], v[r]);
	if(tam%2) // Jogada do Wanderlei
		return memo[l][r] = min(dp(l+1,r), dp(l,r-1));

	// Jogada do Alberto
	return memo[l][r] = max(dp(l+1,r) + v[l], dp(l,r-1) + v[r]);
}

bool solve(){
	cnt++; // Melhor isso do que memset(memo, -1,sizeof(memo));
	int n;
	if(cin.eof()) return true;
	cin >> n;
	if(cin.eof()) return true;

	for(int i=0;i<n;i++) cin >> v[i];

	cout << dp(0,n-1) << "\n";
	return false;
}

int main(){
	ios_base::sync_with_stdio(0);
	cin.tie(0)->tie(0);
	int t = 1;
	// cin >>t;
	while(1){
		if(solve()) break;
	}

	return 0;
}
