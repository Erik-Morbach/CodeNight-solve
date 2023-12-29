#include <bits/stdc++.h>
using namespace std;
typedef long long int ll;
typedef pair<int,int> ii;
typedef vector<int> vi;
#define x first
#define y second
const int maxn = 10000 + 100;

ll v[maxn];

ll memo[maxn][2];

void solve(){
	int n;
	if(cin.eof()) exit(0);
	cin >> n;
	if(cin.eof()) exit(0);

	for(int i=0;i<n;i++) cin >> v[i];

	int oldDp = 0;
	int curDp = 1;

	for(int i=0;i+1<n;i++){
		memo[i][curDp] = max(v[i], v[i+1]);
	}
	swap(curDp, oldDp);
	for(int tam = 3;tam<=n;tam++){ // Mesma ideia da Dp anterior, porém o estado é
								   // memo[indice inicial][tamanho do segmento]
								   // Como o tamanho aumenta de 1 em 1, podemos usar só
								   // O(n) de memória
								   // Obs: durante a competição isso passou usando 
								   // O(n²) de memória
		for(int i=0;i+tam-1<n;i++){
			if(tam%2){
				memo[i][curDp] = min(memo[i+1][oldDp], memo[i][oldDp]);
			}
			else{
				memo[i][curDp] = max(v[i]+memo[i+1][oldDp], memo[i][oldDp] + v[i+tam-1]);
			}
		}
		swap(curDp, oldDp);
	}
	cout << memo[0][oldDp] << "\n";
}

int main(){
	ios_base::sync_with_stdio(0);
	cin.tie(0)->tie(0);
	int t = 1;
	// cin >>t;
	while(1){
		solve();
	}

	return 0;
}
