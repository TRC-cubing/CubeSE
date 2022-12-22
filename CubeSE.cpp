#include <fstream>
#include <iostream>
#include <vector>
#include <stack>
#include <string>
#include <unordered_map>
#include <set>
#include <algorithm>
#include <time.h>
#include <thread>
#include <document.h>
#include <istreamwrapper.h>
#include <unordered_set>
#include <cmath>

using namespace rapidjson;

struct State {
	std::vector<int> cp;
	std::vector<int> co;
	std::vector<int> ep;
	std::vector<int> eo;

	State(std::vector<int> arg_CP = { 0, 1, 2, 3, 4, 5, 6, 7 }, std::vector<int> arg_CO = { 0, 0, 0, 0, 0, 0, 0, 0 }, std::vector<int> arg_EP = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 }, std::vector<int> arg_EO = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }) {
		cp = arg_CP;
		co = arg_CO;
		ep = arg_EP;
		eo = arg_EO;
	}

	State apply_move(State move) {
		std::vector<int> new_cp;
		std::vector<int> new_co;
		std::vector<int> new_ep;
		std::vector<int> new_eo;

		for (int p : move.cp) {
			new_cp.emplace_back(cp[p]);
		}

		for (int i = 0; i < 8; ++i) {
			int p = move.co[i];
			new_co.emplace_back((co[p] + p) % 3);
		}

		for (int p : move.ep) {
			new_ep.emplace_back(ep[p]);
		}

		for (int i = 0; i < 12; ++i) {
			int p = move.eo[i];
			new_eo.emplace_back((eo[p] + p) % 2);
		}

		return State(new_cp, new_co, new_ep, new_eo);
	}
};

struct State_fs {
	std::vector<int> cp;
	std::vector<int> co;
	std::vector<int> ep;
	std::vector<int> eo;
	std::vector<int> center;

	State_fs(std::vector<int> arg_CP = { 0, 1, 2, 3, 4, 5, 6, 7 }, std::vector<int> arg_CO = { 0, 0, 0, 0, 0, 0, 0, 0 }, std::vector<int> arg_EP = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 }, std::vector<int> arg_EO = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }, std::vector<int> arg_CENTER = { 0, 1, 2, 3, 4, 5 }) {
		cp = arg_CP;
		co = arg_CO;
		ep = arg_EP;
		eo = arg_EO;
		center = arg_CENTER;
	}
};

std::unordered_map<int, State> moves = {
	{0 , State({ 3, 0, 1, 2, 4, 5, 6, 7 },
	{ 0, 0, 0, 0, 0, 0, 0, 0 },
	{ 0, 1, 2, 3, 7, 4, 5, 6, 8, 9, 10, 11 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 })},

	{1 , State({ 2, 3, 0, 1, 4, 5, 6, 7 },
	{ 0, 0, 0, 0, 0, 0, 0, 0 },
	{ 0, 1, 2, 3, 6, 7, 4, 5, 8, 9, 10, 11 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 })},

	{2 , State({ 1, 2, 3, 0, 4, 5, 6, 7 },
	{ 0, 0, 0, 0, 0, 0, 0, 0 },
	{ 0, 1, 2, 3, 5, 6, 7, 4, 8, 9, 10, 11 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 })},

	{3 , State({ 0, 1, 2, 3, 5, 6, 7, 4 },
	{ 0, 0, 0, 0, 0, 0, 0, 0 },
	{ 0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 8 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 })},

	{4 , State({ 0, 1, 2, 3, 6, 7, 4, 5 },
	{ 0, 0, 0, 0, 0, 0, 0, 0 },
	{ 0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 8, 9 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 })},

	{5 , State({ 0, 1, 2, 3, 7, 4, 5, 6 },
	{ 0, 0, 0, 0, 0, 0, 0, 0 },
	{ 0, 1, 2, 3, 4, 5, 6, 7, 11, 8, 9, 10 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 })},

	{6 , State({ 4, 1, 2, 0, 7, 5, 6, 3 },
	{ 2, 0, 0, 1, 1, 0, 0, 2 },
	{ 11, 1, 2, 7, 4, 5, 6, 0, 8, 9, 10, 3 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 })},

	{7 , State({ 7, 1, 2, 4, 3, 5, 6, 0 },
	{ 0, 0, 0, 0, 0, 0, 0, 0 },
	{ 3, 1, 2, 0, 4, 5, 6, 11, 8, 9, 10, 7 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 })},

	{8 , State({ 3, 1, 2, 7, 0, 5, 6, 4 },
	{ 2, 0, 0, 1, 1, 0, 0, 2 },
	{ 7, 1, 2, 11, 4, 5, 6, 3, 8, 9, 10, 0 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 })},

	{9 , State({ 0, 2, 6, 3, 4, 1, 5, 7 },
	{ 0, 1, 2, 0, 0, 2, 1, 0 },
	{ 0, 5, 9, 3, 4, 2, 6, 7, 8, 1, 10, 11 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 })},

	{10 , State({ 0, 6, 5, 3, 4, 2, 1, 7 },
	{ 0, 0, 0, 0, 0, 0, 0, 0 },
	{ 0, 2, 1, 3, 4, 9, 6, 7, 8, 5, 10, 11 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 })},

	{11 , State({ 0, 5, 1, 3, 4, 6, 2, 7 },
	{ 0, 1, 2, 0, 0, 2, 1, 0 },
	{ 0, 9, 5, 3, 4, 1, 6, 7, 8, 2, 10, 11 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 })},

	{12 , State({ 0, 1, 3, 7, 4, 5, 2, 6 },
	{ 0, 0, 1, 2, 0, 0, 2, 1 },
	{ 0, 1, 6, 10, 4, 5, 3, 7, 8, 9, 2, 11 },
	{ 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0 })},

	{13 , State({ 0, 1, 7, 6, 4, 5, 3, 2 },
	{ 0, 0, 0, 0, 0, 0, 0, 0 },
	{ 0, 1, 3, 2, 4, 5, 10, 7, 8, 9, 6, 11 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 })},

	{14 , State({ 0, 1, 6, 2, 4, 5, 7, 3 },
	{ 0, 0, 1, 2, 0, 0, 2, 1 },
	{ 0, 1, 10, 6, 4, 5, 2, 7, 8, 9, 3, 11 },
	{ 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0 })},

	{15 , State({ 1, 5, 2, 3, 0, 4, 6, 7 },
	{ 1, 2, 0, 0, 2, 1, 0, 0 },
	{ 4, 8, 2, 3, 1, 5, 6, 7, 0, 9, 10, 11 },
	{ 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0 })},

	{16 , State({ 5, 4, 2, 3, 1, 0, 6, 7 },
	{ 0, 0, 0, 0, 0, 0, 0, 0 },
	{ 1, 0, 2, 3, 8, 5, 6, 7, 4, 9, 10, 11 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 })},

	{17 , State({ 4, 0, 2, 3, 5, 1, 6, 7 },
	{ 1, 2, 0, 0, 2, 1, 0, 0 },
	{ 8, 4, 2, 3, 0, 5, 6, 7, 1, 9, 10, 11 },
	{ 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0 })}
};

std::vector<int> move_name_index = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17 };
std::vector<int> move_name_index_ph2 = { 0, 1, 2, 3, 4, 5, 7, 10, 13, 16 };
std::vector<int> move_name_index_E;

std::vector<std::vector<int>> co_move_table;
std::vector<std::vector<int>> eo_move_table;
std::vector<std::vector<int>> e_combination_table;
std::vector<std::vector<int>> cp_move_table;
std::vector<std::vector<int>> ud_ep_move_table;
std::vector<std::vector<int>> e_ep_move_table;
std::vector<std::vector<int>> co_eec_prune_table;
std::vector<std::vector<int>> eo_eec_prune_table;
std::vector<std::vector<int>> cp_eep_prune_table;
std::vector<std::vector<int>> udep_eep_prune_table;

std::vector<std::vector<int>> co_move_table_E;
std::vector<std::vector<int>> eo_move_table_E;
std::vector<std::vector<int>> cp_move_table_E;
std::vector<std::vector<int>> ep_move_table_E;
std::vector<std::vector<int>> center_move_table_E;

//std::vector<std::vector<int>> co_eo_prune_table_E;
//std::vector<int> cp_prune_table_E;
//std::vector<int> mep_prune_table_E;
//std::vector<int> eep_prune_table_E;
//std::vector<int> sep_prune_table_E;

unsigned char* co_cp_prune_table_E;
unsigned char* co_mep_prune_table_E;
unsigned char* co_eep_prune_table_E;
unsigned char* co_sep_prune_table_E;
unsigned char* co_eo_center_prune_table_E;
unsigned char* co_eo_prune_table_E;
unsigned char* cp_mep_prune_table_E;
unsigned char* cp_eep_prune_table_E;
unsigned char* cp_sep_prune_table_E;
unsigned char* cp_eep_center_prune_table_E;
unsigned char* eo_mep_prune_table_E;
unsigned char* eo_eep_prune_table_E;
unsigned char* eo_sep_prune_table_E;
unsigned char* eo_cp_prune_table_E;
unsigned char* mep_sep_prune_table_E;

std::vector<std::vector<int>> co_center_prune_table_E;
std::vector<std::vector<int>> eo_center_prune_table_E;
std::vector<std::vector<int>> cp_center_prune_table_E;
std::vector<std::vector<int>> mep_center_prune_table_E;
std::vector<std::vector<int>> eep_center_prune_table_E;
std::vector<std::vector<int>> sep_center_prune_table_E;

int forbidden;
int solved_co;
int solved_cp;
int pattern = -1;
unsigned long long nodes = 0;
bool brackets;

std::stack<int> last_solution_length;

std::unordered_set<int> meplist = { 4381, 4471, 4561, 5461, 5551, 6541, 5371, 6361, 7351, 6451, 7441, 7531 };
std::unordered_set<int> seplist = { 4391, 4481, 4571, 5471, 5561, 6551, 5381, 6371, 7361, 6461, 7451, 7541 };
std::unordered_set<int> solved_eo;
std::unordered_set<int> solved_mep;
std::unordered_set<int> solved_eep;
std::unordered_set<int> solved_sep;

std::vector<std::string> x_rotation_move_names;

std::vector<std::vector<bool>> is_move_available = {
	{ false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, true, true, true },
	{ false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, true, true, true },
	{ false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, true, true, true },

	{ false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, true, true, true },
	{ false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, true, true, true },
	{ false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, true, true, true },

	{ true, true, true, true, true, true, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false, true, true, true, true, true, true },
	{ true, true, true, true, true, true, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false, true, true, true, true, true, true },
	{ true, true, true, true, true, true, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false, true, true, true, true, true, true },

	{ true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false, true, true, true, true, true, true },
	{ true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false, true, true, true, true, true, true },
	{ true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false, true, true, true, true, true, true },

	{ true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false },
	{ true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false },
	{ true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false },

	{ true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false },
	{ true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false },
	{ true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false },

	{ true, true, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, true, true, true },
	{ true, false, true, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, true, true, true },
	{ false, true, true, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, true, true, true },

	{ false, false, false, true, true, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, true, true, true },
	{ false, false, false, true, false, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, true, true, true },
	{ false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, true, true, true },

	{ true, true, true, true, true, true, true, true, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false, true, true, true, true, true, true },
	{ true, true, true, true, true, true, true, false, true, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false, true, true, true, true, true, true },
	{ true, true, true, true, true, true, false, true, true, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false, true, true, true, true, true, true },

	{ true, true, true, true, true, true, false, false, false, true, true, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false, true, true, true, true, true, true },
	{ true, true, true, true, true, true, false, false, false, true, false, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false, true, true, true, true, true, true },
	{ true, true, true, true, true, true, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false, true, true, true, true, true, true },

	{ true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false },
	{ true, true, true, true, true, true, true, true, true, true, true, true, true, false, true, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false },
	{ true, true, true, true, true, true, true, true, true, true, true, true, false, true, true, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false },

	{ true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, true, true, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false },
	{ true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, true, false, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false },
	{ true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false },

	{ true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false, true, true, true, true, true, true },
	{ true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false, true, true, true, true, true, true },
	{ true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false, true, true, true, true, true, true },

	{ false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, true, true, true },
	{ false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, true, true, true },
	{ false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, true, true, true },

	{ true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false },
	{ true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false },
	{ true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, true, true, true, true, true, true, false, false, false, false, false, false, true, true, true, true, true, true, false, false, false },
};
//std::unordered_map<int, std::unordered_map<int, bool>> is_move_available_ph2;

std::unordered_map<std::string, std::vector<int>> solved_index1 = {
	{ "co", { 12, 15, 18, 21, 126, 171, 225, 180, 234, 243, 918, 1323, 1458, 1485, 5589 } },
	{ "cp", { 3, 2, 1, 0, 26, 16, 4, 14, 2, 0, 126, 36, 6, 0, 0 } }
};
std::unordered_map<std::string, std::vector<std::unordered_set<int>>> solved_index2 = {
	{ "eo",
		{
			{ 0, 24, 40, 48, 72, 80, 96, 120, 136, 144, 160, 184, 192, 216, 232, 240, 264, 272, 288, 312, 320, 344, 360, 368, 384, 408, 424, 432, 456, 464, 480, 504, 520, 528, 544, 568, 576, 600, 616, 624, 640, 664, 680, 688, 712, 720, 736, 760, 768, 792, 808, 816, 840, 848, 864, 888, 904, 912, 928, 952, 960, 984, 1000, 1008 },
			{ 0, 24, 40, 48, 72, 80, 96, 120, 136, 144, 160, 184, 192, 216, 232, 240, 264, 272, 288, 312, 320, 344, 360, 368, 384, 408, 424, 432, 456, 464, 480, 504, 1032, 1040, 1056, 1080, 1088, 1112, 1128, 1136, 1152, 1176, 1192, 1200, 1224, 1232, 1248, 1272, 1280, 1304, 1320, 1328, 1352, 1360, 1376, 1400, 1416, 1424, 1440, 1464, 1472, 1496, 1512, 1520 },
			{ 0, 24, 40, 48, 72, 80, 96, 120, 136, 144, 160, 184, 192, 216, 232, 240, 520, 528, 544, 568, 576, 600, 616, 624, 640, 664, 680, 688, 712, 720, 736, 760, 1032, 1040, 1056, 1080, 1088, 1112, 1128, 1136, 1152, 1176, 1192, 1200, 1224, 1232, 1248, 1272, 1536, 1560, 1576, 1584, 1608, 1616, 1632, 1656, 1672, 1680, 1696, 1720, 1728, 1752, 1768, 1776 },
			{ 0, 24, 40, 48, 72, 80, 96, 120, 264, 272, 288, 312, 320, 344, 360, 368, 520, 528, 544, 568, 576, 600, 616, 624, 768, 792, 808, 816, 840, 848, 864, 888, 1032, 1040, 1056, 1080, 1088, 1112, 1128, 1136, 1280, 1304, 1320, 1328, 1352, 1360, 1376, 1400, 1536, 1560, 1576, 1584, 1608, 1616, 1632, 1656, 1800, 1808, 1824, 1848, 1856, 1880, 1896, 1904 },
			{ 0, 24, 40, 48, 72, 80, 96, 120, 136, 144, 160, 184, 192, 216, 232, 240, 264, 272, 288, 312, 320, 344, 360, 368, 384, 408, 424, 432, 456, 464, 480, 504 },
			{ 0, 24, 40, 48, 72, 80, 96, 120, 136, 144, 160, 184, 192, 216, 232, 240, 520, 528, 544, 568, 576, 600, 616, 624, 640, 664, 680, 688, 712, 720, 736, 760 },
			{ 0, 24, 40, 48, 72, 80, 96, 120, 264, 272, 288, 312, 320, 344, 360, 368, 520, 528, 544, 568, 576, 600, 616, 624, 768, 792, 808, 816, 840, 848, 864, 888 },
			{ 0, 24, 40, 48, 72, 80, 96, 120, 136, 144, 160, 184, 192, 216, 232, 240, 1032, 1040, 1056, 1080, 1088, 1112, 1128, 1136, 1152, 1176, 1192, 1200, 1224, 1232, 1248, 1272 },
			{ 0, 24, 40, 48, 72, 80, 96, 120, 264, 272, 288, 312, 320, 344, 360, 368, 1032, 1040, 1056, 1080, 1088, 1112, 1128, 1136, 1280, 1304, 1320, 1328, 1352, 1360, 1376, 1400 },
			{ 0, 24, 40, 48, 72, 80, 96, 120, 520, 528, 544, 568, 576, 600, 616, 624, 1032, 1040, 1056, 1080, 1088, 1112, 1128, 1136, 1536, 1560, 1576, 1584, 1608, 1616, 1632, 1656 },
			{ 0, 24, 40, 48, 72, 80, 96, 120, 136, 144, 160, 184, 192, 216, 232, 240 },
			{ 0, 24, 40, 48, 72, 80, 96, 120, 264, 272, 288, 312, 320, 344, 360, 368 },
			{ 0, 24, 40, 48, 72, 80, 96, 120, 520, 528, 544, 568, 576, 600, 616, 624 },
			{ 0, 24, 40, 48, 72, 80, 96, 120, 1032, 1040, 1056, 1080, 1088, 1112, 1128, 1136 },
			{ 0, 24, 40, 48, 72, 80, 96, 120 }
		}
	},
	{ "mep",
		{
			{ 1141, 1231, 1321, 1411, 1501, 1591, 2131, 2221, 2311, 2401, 2491, 2581, 3121, 3211, 3301, 3391, 3481, 3571, 4111, 4201, 4291, 4381, 4471, 4561, 5101, 5191, 5281, 5371, 5461, 5551, 6091, 6181, 6271, 6361, 6451, 6541, 7081, 7171, 7261, 7351, 7441, 7531 },
			{ 151, 241, 331, 421, 511, 601, 2041, 2221, 2311, 2401, 2491, 2581, 3031, 3211, 3301, 3391, 3481, 3571, 4021, 4201, 4291, 4381, 4471, 4561, 5011, 5191, 5281, 5371, 5461, 5551, 6001, 6181, 6271, 6361, 6451, 6541, 6991, 7171, 7261, 7351, 7441, 7531 },
			{ 61, 241, 331, 421, 511, 601, 1051, 1231, 1321, 1411, 1501, 1591, 3031, 3121, 3301, 3391, 3481, 3571, 4021, 4111, 4291, 4381, 4471, 4561, 5011, 5101, 5281, 5371, 5461, 5551, 6001, 6091, 6271, 6361, 6451, 6541, 6991, 7081, 7261, 7351, 7441, 7531 },
			{ 61, 151, 331, 421, 511, 601, 1051, 1141, 1321, 1411, 1501, 1591, 2041, 2131, 2311, 2401, 2491, 2581, 4021, 4111, 4201, 4381, 4471, 4561, 5011, 5101, 5191, 5371, 5461, 5551, 6001, 6091, 6181, 6361, 6451, 6541, 6991, 7081, 7171, 7351, 7441, 7531 },
			{ 2221, 2311, 2401, 2491, 2581, 3211, 3301, 3391, 3481, 3571, 4201, 4291, 4381, 4471, 4561, 5191, 5281, 5371, 5461, 5551, 6181, 6271, 6361, 6451, 6541, 7171, 7261, 7351, 7441, 7531 },
			{ 1231, 1321, 1411, 1501, 1591, 3121, 3301, 3391, 3481, 3571, 4111, 4291, 4381, 4471, 4561, 5101, 5281, 5371, 5461, 5551, 6091, 6271, 6361, 6451, 6541, 7081, 7261, 7351, 7441, 7531 },
			{ 1141, 1321, 1411, 1501, 1591, 2131, 2311, 2401, 2491, 2581, 4111, 4201, 4381, 4471, 4561, 5101, 5191, 5371, 5461, 5551, 6091, 6181, 6361, 6451, 6541, 7081, 7171, 7351, 7441, 7531 },
			{ 241, 331, 421, 511, 601, 3031, 3301, 3391, 3481, 3571, 4021, 4291, 4381, 4471, 4561, 5011, 5281, 5371, 5461, 5551, 6001, 6271, 6361, 6451, 6541, 6991, 7261, 7351, 7441, 7531 },
			{ 151, 331, 421, 511, 601, 2041, 2311, 2401, 2491, 2581, 4021, 4201, 4381, 4471, 4561, 5011, 5191, 5371, 5461, 5551, 6001, 6181, 6361, 6451, 6541, 6991, 7171, 7351, 7441, 7531 },
			{ 61, 331, 421, 511, 601, 1051, 1321, 1411, 1501, 1591, 4021, 4111, 4381, 4471, 4561, 5011, 5101, 5371, 5461, 5551, 6001, 6091, 6361, 6451, 6541, 6991, 7081, 7351, 7441, 7531 },
			{ 3301, 3391, 3481, 3571, 4291, 4381, 4471, 4561, 5281, 5371, 5461, 5551, 6271, 6361, 6451, 6541, 7261, 7351, 7441, 7531 },
			{ 2311, 2401, 2491, 2581, 4201, 4381, 4471, 4561, 5191, 5371, 5461, 5551, 6181, 6361, 6451, 6541, 7171, 7351, 7441, 7531 },
			{ 1321, 1411, 1501, 1591, 4111, 4381, 4471, 4561, 5101, 5371, 5461, 5551, 6091, 6361, 6451, 6541, 7081, 7351, 7441, 7531 },
			{ 331, 421, 511, 601, 4021, 4381, 4471, 4561, 5011, 5371, 5461, 5551, 6001, 6361, 6451, 6541, 6991, 7351, 7441, 7531 },
			{ 4381, 4471, 4561, 5371, 5461, 5551, 6361, 6451, 6541, 7351, 7441, 7531 }
		}
	},
	{ "eep",
		{
			{ 0, 1, 2, 3, 4, 9, 10, 11, 12, 13, 18, 19, 20, 21, 22, 27, 28, 29, 30, 31, 36, 37, 38, 39, 40, 45, 46, 47, 48, 49, 90, 91, 92, 93, 94, 99, 100, 101, 102, 103, 108, 109, 110, 111, 112, 117, 118, 119, 120, 121, 126, 127, 128, 129, 130, 135, 136, 137, 138, 139, 180, 181, 182, 183, 184, 189, 190, 191, 192, 193, 198, 199, 200, 201, 202, 207, 208, 209, 210, 211, 216, 217, 218, 219, 220, 225, 226, 227, 228, 229, 270, 271, 272, 273, 274, 279, 280, 281, 282, 283, 288, 289, 290, 291, 292, 297, 298, 299, 300, 301, 306, 307, 308, 309, 310, 315, 316, 317, 318, 319, 360, 361, 362, 363, 364, 369, 370, 371, 372, 373, 378, 379, 380, 381, 382, 387, 388, 389, 390, 391, 396, 397, 398, 399, 400, 405, 406, 407, 408, 409, 450, 451, 452, 453, 454, 459, 460, 461, 462, 463, 468, 469, 470, 471, 472, 477, 478, 479, 480, 481, 486, 487, 488, 489, 490, 495, 496, 497, 498, 499, 540, 541, 542, 543, 544, 549, 550, 551, 552, 553, 558, 559, 560, 561, 562, 567, 568, 569, 570, 571, 576, 577, 578, 579, 580, 585, 586, 587, 588, 589 },
			{ 0, 1, 2, 3, 4, 9, 10, 11, 12, 13, 18, 19, 20, 21, 22, 27, 28, 29, 30, 31, 36, 37, 38, 39, 40, 45, 46, 47, 48, 49, 2070, 2071, 2072, 2073, 2074, 2079, 2080, 2081, 2082, 2083, 2088, 2089, 2090, 2091, 2092, 2097, 2098, 2099, 2100, 2101, 2106, 2107, 2108, 2109, 2110, 2115, 2116, 2117, 2118, 2119, 3060, 3061, 3062, 3063, 3064, 3069, 3070, 3071, 3072, 3073, 3078, 3079, 3080, 3081, 3082, 3087, 3088, 3089, 3090, 3091, 3096, 3097, 3098, 3099, 3100, 3105, 3106, 3107, 3108, 3109, 4050, 4051, 4052, 4053, 4054, 4059, 4060, 4061, 4062, 4063, 4068, 4069, 4070, 4071, 4072, 4077, 4078, 4079, 4080, 4081, 4086, 4087, 4088, 4089, 4090, 4095, 4096, 4097, 4098, 4099, 5040, 5041, 5042, 5043, 5044, 5049, 5050, 5051, 5052, 5053, 5058, 5059, 5060, 5061, 5062, 5067, 5068, 5069, 5070, 5071, 5076, 5077, 5078, 5079, 5080, 5085, 5086, 5087, 5088, 5089, 6030, 6031, 6032, 6033, 6034, 6039, 6040, 6041, 6042, 6043, 6048, 6049, 6050, 6051, 6052, 6057, 6058, 6059, 6060, 6061, 6066, 6067, 6068, 6069, 6070, 6075, 6076, 6077, 6078, 6079, 7020, 7021, 7022, 7023, 7024, 7029, 7030, 7031, 7032, 7033, 7038, 7039, 7040, 7041, 7042, 7047, 7048, 7049, 7050, 7051, 7056, 7057, 7058, 7059, 7060, 7065, 7066, 7067, 7068, 7069 },
			{ 0, 1, 2, 3, 4, 189, 190, 191, 192, 193, 279, 280, 281, 282, 283, 369, 370, 371, 372, 373, 459, 460, 461, 462, 463, 549, 550, 551, 552, 553, 990, 991, 992, 993, 994, 1179, 1180, 1181, 1182, 1183, 1269, 1270, 1271, 1272, 1273, 1359, 1360, 1361, 1362, 1363, 1449, 1450, 1451, 1452, 1453, 1539, 1540, 1541, 1542, 1543, 2979, 2980, 2981, 2982, 2983, 3069, 3070, 3071, 3072, 3073, 3258, 3259, 3260, 3261, 3262, 3348, 3349, 3350, 3351, 3352, 3438, 3439, 3440, 3441, 3442, 3528, 3529, 3530, 3531, 3532, 3969, 3970, 3971, 3972, 3973, 4059, 4060, 4061, 4062, 4063, 4248, 4249, 4250, 4251, 4252, 4338, 4339, 4340, 4341, 4342, 4428, 4429, 4430, 4431, 4432, 4518, 4519, 4520, 4521, 4522, 4959, 4960, 4961, 4962, 4963, 5049, 5050, 5051, 5052, 5053, 5238, 5239, 5240, 5241, 5242, 5328, 5329, 5330, 5331, 5332, 5418, 5419, 5420, 5421, 5422, 5508, 5509, 5510, 5511, 5512, 5949, 5950, 5951, 5952, 5953, 6039, 6040, 6041, 6042, 6043, 6228, 6229, 6230, 6231, 6232, 6318, 6319, 6320, 6321, 6322, 6408, 6409, 6410, 6411, 6412, 6498, 6499, 6500, 6501, 6502, 6939, 6940, 6941, 6942, 6943, 7029, 7030, 7031, 7032, 7033, 7218, 7219, 7220, 7221, 7222, 7308, 7309, 7310, 7311, 7312, 7398, 7399, 7400, 7401, 7402, 7488, 7489, 7490, 7491, 7492 },
			{ 0, 19, 28, 37, 46, 90, 109, 118, 127, 136, 271, 280, 299, 308, 317, 361, 370, 389, 398, 407, 451, 460, 479, 488, 497, 541, 550, 569, 578, 587, 990, 1009, 1018, 1027, 1036, 1080, 1099, 1108, 1117, 1126, 1261, 1270, 1289, 1298, 1307, 1351, 1360, 1379, 1388, 1397, 1441, 1450, 1469, 1478, 1487, 1531, 1540, 1559, 1568, 1577, 1980, 1999, 2008, 2017, 2026, 2070, 2089, 2098, 2107, 2116, 2251, 2260, 2279, 2288, 2297, 2341, 2350, 2369, 2378, 2387, 2431, 2440, 2459, 2468, 2477, 2521, 2530, 2549, 2558, 2567, 3961, 3970, 3989, 3998, 4007, 4051, 4060, 4079, 4088, 4097, 4141, 4150, 4169, 4178, 4187, 4322, 4331, 4340, 4359, 4368, 4412, 4421, 4430, 4449, 4458, 4502, 4511, 4520, 4539, 4548, 4951, 4960, 4979, 4988, 4997, 5041, 5050, 5069, 5078, 5087, 5131, 5140, 5159, 5168, 5177, 5312, 5321, 5330, 5349, 5358, 5402, 5411, 5420, 5439, 5448, 5492, 5501, 5510, 5529, 5538, 5941, 5950, 5969, 5978, 5987, 6031, 6040, 6059, 6068, 6077, 6121, 6130, 6149, 6158, 6167, 6302, 6311, 6320, 6339, 6348, 6392, 6401, 6410, 6429, 6438, 6482, 6491, 6500, 6519, 6528, 6931, 6940, 6959, 6968, 6977, 7021, 7030, 7049, 7058, 7067, 7111, 7120, 7139, 7148, 7157, 7292, 7301, 7310, 7329, 7338, 7382, 7391, 7400, 7419, 7428, 7472, 7481, 7490, 7509, 7518 },
			{ 0, 1, 2, 3, 4, 9, 10, 11, 12, 13, 18, 19, 20, 21, 22, 27, 28, 29, 30, 31, 36, 37, 38, 39, 40, 45, 46, 47, 48, 49 },
			{ 0, 1, 2, 3, 4, 189, 190, 191, 192, 193, 279, 280, 281, 282, 283, 369, 370, 371, 372, 373, 459, 460, 461, 462, 463, 549, 550, 551, 552, 553 },
			{ 0, 19, 28, 37, 46, 90, 109, 118, 127, 136, 271, 280, 299, 308, 317, 361, 370, 389, 398, 407, 451, 460, 479, 488, 497, 541, 550, 569, 578, 587 },
			{ 0, 1, 2, 3, 4, 3069, 3070, 3071, 3072, 3073, 4059, 4060, 4061, 4062, 4063, 5049, 5050, 5051, 5052, 5053, 6039, 6040, 6041, 6042, 6043, 7029, 7030, 7031, 7032, 7033 },
			{ 0, 19, 28, 37, 46, 2070, 2089, 2098, 2107, 2116, 4051, 4060, 4079, 4088, 4097, 5041, 5050, 5069, 5078, 5087, 6031, 6040, 6059, 6068, 6077, 7021, 7030, 7049, 7058, 7067 },
			{ 0, 280, 370, 460, 550, 990, 1270, 1360, 1450, 1540, 3970, 4060, 4340, 4430, 4520, 4960, 5050, 5330, 5420, 5510, 5950, 6040, 6320, 6410, 6500, 6940, 7030, 7310, 7400, 7490 },
			{ 0, 1, 2, 3, 4 },
			{ 0, 19, 28, 37, 46 },
			{ 0, 280, 370, 460, 550 },
			{ 0, 4060, 5050, 6040, 7030 },
			{ 0 }
		}
	},
	{ "sep", 
		{
			{ 1151, 1241, 1331, 1421, 1511, 1601, 2141, 2231, 2321, 2411, 2501, 2591, 3131, 3221, 3311, 3401, 3491, 3581, 4121, 4211, 4301, 4391, 4481, 4571, 5111, 5201, 5291, 5381, 5471, 5561, 6101, 6191, 6281, 6371, 6461, 6551, 7091, 7181, 7271, 7361, 7451, 7541 },
			{ 161, 251, 341, 431, 521, 611, 2051, 2231, 2321, 2411, 2501, 2591, 3041, 3221, 3311, 3401, 3491, 3581, 4031, 4211, 4301, 4391, 4481, 4571, 5021, 5201, 5291, 5381, 5471, 5561, 6011, 6191, 6281, 6371, 6461, 6551, 7001, 7181, 7271, 7361, 7451, 7541 },
			{ 71, 251, 341, 431, 521, 611, 1061, 1241, 1331, 1421, 1511, 1601, 3041, 3131, 3311, 3401, 3491, 3581, 4031, 4121, 4301, 4391, 4481, 4571, 5021, 5111, 5291, 5381, 5471, 5561, 6011, 6101, 6281, 6371, 6461, 6551, 7001, 7091, 7271, 7361, 7451, 7541 },
			{ 71, 161, 341, 431, 521, 611, 1061, 1151, 1331, 1421, 1511, 1601, 2051, 2141, 2321, 2411, 2501, 2591, 4031, 4121, 4211, 4391, 4481, 4571, 5021, 5111, 5201, 5381, 5471, 5561, 6011, 6101, 6191, 6371, 6461, 6551, 7001, 7091, 7181, 7361, 7451, 7541 },
			{ 2231, 2321, 2411, 2501, 2591, 3221, 3311, 3401, 3491, 3581, 4211, 4301, 4391, 4481, 4571, 5201, 5291, 5381, 5471, 5561, 6191, 6281, 6371, 6461, 6551, 7181, 7271, 7361, 7451, 7541 },
			{ 1241, 1331, 1421, 1511, 1601, 3131, 3311, 3401, 3491, 3581, 4121, 4301, 4391, 4481, 4571, 5111, 5291, 5381, 5471, 5561, 6101, 6281, 6371, 6461, 6551, 7091, 7271, 7361, 7451, 7541 },
			{ 1151, 1331, 1421, 1511, 1601, 2141, 2321, 2411, 2501, 2591, 4121, 4211, 4391, 4481, 4571, 5111, 5201, 5381, 5471, 5561, 6101, 6191, 6371, 6461, 6551, 7091, 7181, 7361, 7451, 7541 },
			{ 251, 341, 431, 521, 611, 3041, 3311, 3401, 3491, 3581, 4031, 4301, 4391, 4481, 4571, 5021, 5291, 5381, 5471, 5561, 6011, 6281, 6371, 6461, 6551, 7001, 7271, 7361, 7451, 7541 },
			{ 161, 341, 431, 521, 611, 2051, 2321, 2411, 2501, 2591, 4031, 4211, 4391, 4481, 4571, 5021, 5201, 5381, 5471, 5561, 6011, 6191, 6371, 6461, 6551, 7001, 7181, 7361, 7451, 7541 },
			{ 71, 341, 431, 521, 611, 1061, 1331, 1421, 1511, 1601, 4031, 4121, 4391, 4481, 4571, 5021, 5111, 5381, 5471, 5561, 6011, 6101, 6371, 6461, 6551, 7001, 7091, 7361, 7451, 7541 },
			{ 3311, 3401, 3491, 3581, 4301, 4391, 4481, 4571, 5291, 5381, 5471, 5561, 6281, 6371, 6461, 6551, 7271, 7361, 7451, 7541 },
			{ 2321, 2411, 2501, 2591, 4211, 4391, 4481, 4571, 5201, 5381, 5471, 5561, 6191, 6371, 6461, 6551, 7181, 7361, 7451, 7541 },
			{ 1331, 1421, 1511, 1601, 4121, 4391, 4481, 4571, 5111, 5381, 5471, 5561, 6101, 6371, 6461, 6551, 7091, 7361, 7451, 7541 },
			{ 341, 431, 521, 611, 4031, 4391, 4481, 4571, 5021, 5381, 5471, 5561, 6011, 6371, 6461, 6551, 7001, 7361, 7451, 7541 },
			{ 4391, 4481, 4571, 5381, 5471, 5561, 6371, 6461, 6551, 7361, 7451, 7541 }
		}
	}
};

inline int co_to_index(std::vector<int> co) {
	int index = 0;
	for (int i = 0; i < 7; ++i) {
		index *= 3;
		index += co[i];
	}
	return index;
}

inline int eo_to_index(std::vector<int> eo) {
	int index = 0;
	for (int i = 0; i < 11; ++i) {
		index *= 2;
		index += eo[i];
	}
	return index;
}

inline int calc_combination(int n, int r) {
	int ret = 1;
	for (int i = 0; i < r; ++i) {
		ret *= n - i;
	}
	for (int i = 0; i < r; ++i) {
		ret /= r - i;
	}

	return ret;
}

inline int e_combination_to_index(std::vector<int> ep) {
	std::stack<int> e_combination;
	int index = 0;
	int r = 4;
	for (int e : ep) {
		if (e == 0 || e == 1 || e == 2 || e == 3) {
			e_combination.push(1);
		}
		else {
			e_combination.push(0);
		}
	}
	for (int i = 11; i > -1; --i) {
		if (e_combination.top()) {
			//std::cout << e_combination.top();
			index += calc_combination(i, r);
			--r;
			e_combination.pop();
		}
		else {
			e_combination.pop();
		}
	}
	return index;
}

inline int cp_to_index(std::vector<int> cp) {
	int index = 0;
	for (int i = 0; i < 8; ++i) {
		index *= (8 - i);
		for (int j = i + 1; j < 8; ++j) {
			if (cp[i] > cp[j]) {
				++index;
			}
		}
	}
	return index;
}

inline int ud_ep_to_index(std::vector<int> ep) {
	int index = 0;
	for (int i = 0; i < 8; ++i) {
		index *= 8 - i;
		for (int j = i + 1; j < 8; ++j) {
			if (ep[i + 4] > ep[j + 4]) {
				++index;
			}
		}
	}
	return index;
}

inline int e_ep_to_index(std::vector<int> ep) {
	int index = 0;
	for (int i = 0; i < 4; ++i) {
		index *= 4 - i;
		for (int j = i + 1; j < 4; ++j) {
			if (ep[i] > ep[j]) {
				++index;
			}
		}
	}
	return index;
}

inline int MEP_to_index(std::vector<int> ep) {
	std::vector<int>::iterator w;
	std::vector<int>::iterator x;
	std::vector<int>::iterator y;
	std::vector<int>::iterator z;

	w = std::find(ep.begin(), ep.end(), 4);
	x = std::find(ep.begin(), ep.end(), 6);
	y = std::find(ep.begin(), ep.end(), 8);
	z = std::find(ep.begin(), ep.end(), 10);

	int i = std::distance(ep.begin(), w);
	int j = std::distance(ep.begin(), x);
	int k = std::distance(ep.begin(), y);
	int l = std::distance(ep.begin(), z);

	std::vector<int> mep0 = { i, j, k, l };

	int m = 0;
	int n = 0;

	int a = i;
	int b = j;
	int c = k;
	int d = l;

	a *= 990;

	if (i > j) {
		b *= 90;
	}
	else {
		b = (b - 1) * 90;
	}

	for (int p = 0; p < 2; ++p) {
		if (k > mep0[p]) {
			++m;
		}
	}

	c = (c - m) * 9;

	for (int q = 0; q < 3; ++q) {
		if (l > mep0[q]) {
			++n;
		}
	}

	d -= n;

	return a + b + c + d;
}

inline int EEP_to_index(std::vector<int> ep) {
	std::vector<int>::iterator w;
	std::vector<int>::iterator x;
	std::vector<int>::iterator y;
	std::vector<int>::iterator z;

	w = std::find(ep.begin(), ep.end(), 0);
	x = std::find(ep.begin(), ep.end(), 1);
	y = std::find(ep.begin(), ep.end(), 2);
	z = std::find(ep.begin(), ep.end(), 3);

	int i = std::distance(ep.begin(), w);
	int j = std::distance(ep.begin(), x);
	int k = std::distance(ep.begin(), y);
	int l = std::distance(ep.begin(), z);

	std::vector<int> eep0 = { i, j, k, l };

	int m = 0;
	int n = 0;

	int a = i;
	int b = j;
	int c = k;
	int d = l;

	a *= 990;

	if (i > j) {
		b *= 90;
	}
	else {
		b = (b - 1) * 90;
	}

	for (int p = 0; p < 2; ++p) {
		if (k > eep0[p]) {
			++m;
		}
	}

	c = (c - m) * 9;

	for (int q = 0; q < 3; ++q) {
		if (l > eep0[q]) {
			++n;
		}
	}

	d -= n;

	return a + b + c + d;
}

inline int SEP_to_index(std::vector<int> ep) {
	std::vector<int>::iterator w;
	std::vector<int>::iterator x;
	std::vector<int>::iterator y;
	std::vector<int>::iterator z;

	w = std::find(ep.begin(), ep.end(), 5);
	x = std::find(ep.begin(), ep.end(), 7);
	y = std::find(ep.begin(), ep.end(), 9);
	z = std::find(ep.begin(), ep.end(), 11);

	int i = std::distance(ep.begin(), w);
	int j = std::distance(ep.begin(), x);
	int k = std::distance(ep.begin(), y);
	int l = std::distance(ep.begin(), z);

	std::vector<int> sep0 = { i, j, k, l };

	int m = 0;
	int n = 0;

	int a = i;
	int b = j;
	int c = k;
	int d = l;

	a *= 990;

	if (i > j) {
		b *= 90;
	}
	else {
		b = (b - 1) * 90;
	}

	for (int p = 0; p < 2; ++p) {
		if (k > sep0[p]) {
			++m;
		}
	}

	c = (c - m) * 9;

	for (int q = 0; q < 3; ++q) {
		if (l > sep0[q]) {
			++n;
		}
	}

	d -= n;

	return a + b + c + d;
}

inline int center_to_index(std::vector<int> center) {
	int i = center[0];
	int j = center[2];
	int k = 0;

	std::vector<int> new_list(center.begin() + 2, center.end());

	while (*std::min_element(new_list.begin(), new_list.end()) != j) {
		new_list.erase(std::min_element(new_list.begin(), new_list.end()));
		++k;
	}

	return i * 4 + k;
}

inline int OLL_cp_permutation_to_index(std::vector<int> cp) {
	int index = 0;
	for (int i = 0; i < 4; ++i) {
		index *= 4 - i;
		for (int j = i + 1; j < 4; ++j) {
			if (cp[i] > cp[j]) {
				++index;
			}
		}
	}
	return index;
}

inline int OLL_cp_to_index(std::vector<int> OLL_cp) {
	int index = 0;
	int r = 4;
	for (int i = 7; i > -1; --i) {
		if (OLL_cp[i] == -1) {
			index += calc_combination(i, r);
			--r;
		}
	}
	std::vector<int> permutation_list;
	for (int i : OLL_cp) {
		if (i != -1) {
			permutation_list.emplace_back(i);
		}
	}
	int p = OLL_cp_permutation_to_index(permutation_list);
	return index * 24 + p;
}

inline int F2L_co_to_index(std::vector<int> F2L_co) {
	int index = 0;
	int r = pattern + 1;
	std::stack<int> co_stack;
	for (int i = 7; i > -1; --i) {
		if (F2L_co[i] != -1) {
			co_stack.push(F2L_co[i]);
			index += calc_combination(i, r);
			--r;
		}
	}

	index = index * int(std::pow(3, co_stack.size()));

	for (int i = co_stack.size() - 1; i > -1; --i) {
		index += co_stack.top() * int(std::pow(3, i));
		co_stack.pop();
	}

	return index;
}

inline int F2L_cp_to_index(std::vector<int> F2L_cp) {
	int index = 0;
	int index2 = 0;
	int r = 7 - pattern;
	int s = pattern + 1;
	std::vector<int> permutation_list;

	for (int i = 7; i > -1; --i) {
		if (F2L_cp[i] == -1) {
			index += calc_combination(i, r);
			--r;
		}
	}

	for (int i : F2L_cp) {
		if (i != -1) {
			permutation_list.emplace_back(i);
		}
	}

	for (int i = 0; i < permutation_list.size(); ++i) {
		index2 *= s - i;
		for (int j = i + 1; j < s; ++j) {
			if (permutation_list[i] > permutation_list[j]) {
				++index2;
			}
		}
	}

	for (int i = s; i > 1; --i) {
		index *= i;
	}

	return index + index2;
}

struct Search_PLL0 {

	State initial_state;

	int max_solution_length;
	int solutions;
	int count = 0;

	std::vector<int> current_solution;
	int next_co_index;
	int next_eo_index;
	int next_cp_index;
	int next_mep_index;
	int next_eep_index;
	int next_sep_index;

	bool found;

	std::unordered_map<int, int> inv = { { 0, 3 }, { 12, 15 }, { 15, 12 } };
	std::set<int> auf_adf = { forbidden, forbidden + 1, forbidden + 2, inv[forbidden], inv[forbidden] + 1, inv[forbidden] + 2 };

	std::string solution;
	std::vector<std::string> move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'",
											"R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" };
	Search_PLL0(State arg_state) {
		initial_state = arg_state;
	}

	bool limited_search_PLL(int co_index, int eo_index, int cp_index, int mep_index, int eep_index, int sep_index, int depth) {
		found = false;
		if (depth == 0 && co_index == 0 && eo_index == 0 && cp_index == 0 && mep_index == 4471 && eep_index == 0 && sep_index == 5561) {
			if (brackets) {
				for (int sol : current_solution) {
					solution += move_names[sol];
					solution += " ";
				}
			}
			else {
				for (int i = 0; i < current_solution.size() - 2; ++i) {
					solution += move_names[current_solution[i]];
					solution += " ";
				}
				if (auf_adf.contains(current_solution[current_solution.size() - 2]) && auf_adf.contains(current_solution[current_solution.size() - 1])) {
					solution += "(";
					solution += move_names[current_solution[current_solution.size() - 2]];
					solution += " ";
					solution += move_names[current_solution[current_solution.size() - 1]];
					solution += ")";
				}
				else if (auf_adf.contains(current_solution[current_solution.size() - 1])) {
					solution += move_names[current_solution[current_solution.size() - 2]];
					solution += " (";
					solution += move_names[current_solution[current_solution.size() - 1]];
					solution += ")";
				}
				else {
					solution += move_names[current_solution[current_solution.size() - 2]];
					solution += " ";
					solution += move_names[current_solution[current_solution.size() - 1]];
				}
			}
			++count;
			if (count > solutions) {
				exit(0);
			}
			std::cout << solution << std::endl;
			solution = "";

			return true;
		}

		if (depth == 0) {
			return false;
		}

		if (std::max({ (((co_index * 40320 + cp_index) % 2 == 0) ? (co_cp_prune_table_E[(co_index * 40320 + cp_index) / 2] >> 4) : (co_cp_prune_table_E[(co_index * 40320 + cp_index) / 2] & 0b00001111)),
						(((cp_index * 11880 + mep_index) % 2 == 0) ? (cp_mep_prune_table_E[(cp_index * 11880 + mep_index) / 2] >> 4) : (cp_mep_prune_table_E[(cp_index * 11880 + mep_index) / 2] & 0b00001111)),
						(((cp_index * 11880 + eep_index) % 2 == 0) ? (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] >> 4) : (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] & 0b00001111)),
						(((cp_index * 11880 + sep_index) % 2 == 0) ? (cp_sep_prune_table_E[(cp_index * 11880 + sep_index) / 2] >> 4) : (cp_sep_prune_table_E[(cp_index * 11880 + sep_index) / 2] & 0b00001111)) }) > depth) {
			return false;
		}
		int prev_move;
		if (!(current_solution.empty())) {
			prev_move = current_solution.back();
		}
		else {
			prev_move = -1;
		}

		for (int move_num : move_name_index_E) {
			if (prev_move == -1) {
				if (move_num == forbidden || move_num == (forbidden + 1) || move_num == (forbidden + 2)) {
					continue;
				}
				else {
					goto PASS;
				}
			}
			if (!(is_move_available[prev_move][move_num])) {
				continue;
			}
		PASS:
			current_solution.push_back(move_num);
			next_co_index = co_move_table_E[co_index][move_num];
			next_eo_index = eo_move_table_E[eo_index][move_num];
			next_cp_index = cp_move_table_E[cp_index][move_num];
			next_mep_index = ep_move_table_E[mep_index][move_num];
			next_eep_index = ep_move_table_E[eep_index][move_num];
			next_sep_index = ep_move_table_E[sep_index][move_num];
			limited_search_PLL(next_co_index, next_eo_index, next_cp_index, next_mep_index, next_eep_index, next_sep_index, depth - 1);
			current_solution.pop_back();
		}
		return false;
	}

	void start_search(int min_length, int max_length, int sol_num) {
		max_solution_length = max_length;
		solutions = sol_num;
		int co_index = co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int cp_index = cp_to_index(initial_state.cp);
		int mep_index = MEP_to_index(initial_state.ep);
		int eep_index = EEP_to_index(initial_state.ep);
		int sep_index = SEP_to_index(initial_state.ep);
		int min_depth = min_length;
		if (pattern == 0) {
			move_names = x_rotation_move_names;
		}

		while (min_depth <= max_solution_length) {
			std::cout << "\nstart searching in depth" << min_depth << "\n" << std::endl;
			if (limited_search_PLL(co_index, eo_index, cp_index, mep_index, eep_index, sep_index, min_depth)) {
				;
			}
			++min_depth;
		}
		return;
	}

};

struct Search_PLL1 {

	State initial_state;

	int max_solution_length;
	int solutions;
	int count = 0;

	std::vector<int> current_solution;
	int next_co_index;
	int next_eo_index;
	int next_cp_index;
	int next_mep_index;
	int next_eep_index;
	int next_sep_index;

	bool found;

	std::unordered_map<int, int> inv = { { 0, 3 }, { 12, 15 }, { 15, 12 } };
	std::set<int> auf_adf = { forbidden, forbidden + 2, inv[forbidden], inv[forbidden] + 2 };

	std::string solution;

	std::vector<std::string> move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'",
											"R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" };
	Search_PLL1(State arg_state) {
		initial_state = arg_state;
	}

	bool limited_search_PLL(int co_index, int eo_index, int cp_index, int mep_index, int eep_index, int sep_index, int depth) {
		found = false;
		if (depth == 0 && co_index == 0 && eo_index == 0 && cp_index == 0 && mep_index == 4471 && eep_index == 0 && sep_index == 5561) {
			if (brackets) {
				for (int sol : current_solution) {
					solution += move_names[sol];
					solution += " ";
				}
			}
			else {
				for (int i = 0; i < current_solution.size() - 2; ++i) {
					solution += move_names[current_solution[i]];
					solution += " ";
				}
				if (auf_adf.contains(current_solution[current_solution.size() - 2]) && auf_adf.contains(current_solution[current_solution.size() - 1])) {
					solution += "(";
					solution += move_names[current_solution[current_solution.size() - 2]];
					solution += " ";
					solution += move_names[current_solution[current_solution.size() - 1]];
					solution += ")";
				}
				else if (auf_adf.contains(current_solution[current_solution.size() - 1])) {
					solution += move_names[current_solution[current_solution.size() - 2]];
					solution += " (";
					solution += move_names[current_solution[current_solution.size() - 1]];
					solution += ")";
				}
				else {
					solution += move_names[current_solution[current_solution.size() - 2]];
					solution += " ";
					solution += move_names[current_solution[current_solution.size() - 1]];
				}
			}
			++count;
			if (count > solutions) {
				exit(0);
			}
			std::cout << solution << std::endl;
			solution = "";

			return true;
		}

		if (depth == 0) {
			return false;
		}

		if (std::max({ (((co_index * 40320 + cp_index) % 2 == 0) ? (co_cp_prune_table_E[(co_index * 40320 + cp_index) / 2] >> 4) : (co_cp_prune_table_E[(co_index * 40320 + cp_index) / 2] & 0b00001111)),
						(((cp_index * 11880 + mep_index) % 2 == 0) ? (cp_mep_prune_table_E[(cp_index * 11880 + mep_index) / 2] >> 4) : (cp_mep_prune_table_E[(cp_index * 11880 + mep_index) / 2] & 0b00001111)),
						(((cp_index * 11880 + eep_index) % 2 == 0) ? (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] >> 4) : (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] & 0b00001111)),
						(((cp_index * 11880 + sep_index) % 2 == 0) ? (cp_sep_prune_table_E[(cp_index * 11880 + sep_index) / 2] >> 4) : (cp_sep_prune_table_E[(cp_index * 11880 + sep_index) / 2] & 0b00001111)) }) > depth) {
			return false;
		}

		int prev_move;
		if (!(current_solution.empty())) {
			prev_move = current_solution.back();
		}
		else {
			prev_move = -1;
		}

		for (int move_num : move_name_index_E) {
			if (prev_move == -1) {
				if (move_num == forbidden ||  move_num == (forbidden + 2)) {
					continue;
				}
				else {
					goto PASS;
				}
			}
			if (!(is_move_available[prev_move][move_num])) {
				continue;
			}
		PASS:

			current_solution.push_back(move_num);
			next_co_index = co_move_table_E[co_index][move_num];
			next_eo_index = eo_move_table_E[eo_index][move_num];
			next_cp_index = cp_move_table_E[cp_index][move_num];
			next_mep_index = ep_move_table_E[mep_index][move_num];
			next_eep_index = ep_move_table_E[eep_index][move_num];
			next_sep_index = ep_move_table_E[sep_index][move_num];
			limited_search_PLL(next_co_index, next_eo_index, next_cp_index, next_mep_index, next_eep_index, next_sep_index, depth - 1);
			current_solution.pop_back();
		}
		return false;
	}

	void start_search(int min_length, int max_length, int sol_num) {
		max_solution_length = max_length;
		solutions = sol_num;
		int co_index = co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int cp_index = cp_to_index(initial_state.cp);
		int mep_index = MEP_to_index(initial_state.ep);
		int eep_index = EEP_to_index(initial_state.ep);
		int sep_index = SEP_to_index(initial_state.ep);
		int min_depth = min_length;
		if (pattern == 0) {
			move_names = x_rotation_move_names;
		}

		while (min_depth <= max_solution_length) {
			std::cout << "\nstart searching in depth" << min_depth << "\n" << std::endl;
			if (limited_search_PLL(co_index, eo_index, cp_index, mep_index, eep_index, sep_index, min_depth)) {
				;
			}
			++min_depth;
		}
		return;
	}

};

struct Search_PLL2 {

	State_fs initial_state;

	int max_solution_length;
	int solutions;
	int count = 0;

	std::vector<int> current_solution;
	int next_co_index;
	int next_eo_index;
	int next_cp_index;
	int next_mep_index;
	int next_eep_index;
	int next_sep_index;
	int next_center_index;

	bool found;

	std::unordered_map<int, int> inv = { { 0, 3 }, { 12, 15 }, { 15, 12 } };
	std::set<int> auf_adf = { forbidden, forbidden + 1, forbidden + 2, inv[forbidden], inv[forbidden] + 1, inv[forbidden] + 2 };

	std::string solution;

	std::vector<std::string> move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'",
											"R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" ,
											"Uw", "Uw2", "Uw'", "Dw", "Dw2", "Dw'", "Lw", "Lw2", "Lw'",
											"Rw", "Rw2", "Rw'", "Fw", "Fw2", "Fw'", "Bw", "Bw2", "Bw'",
											"M", "M2", "M'", "E", "E2", "E'", "S", "S2", "S'" };
	Search_PLL2(State_fs arg_state) {
		initial_state = arg_state;
	}

	bool limited_search_PLL_fs(int co_index, int eo_index, int cp_index, int mep_index, int eep_index, int sep_index, int center_index, int depth) {
		found = false;
		if (depth == 0 && co_index == 0 && eo_index == 0 && cp_index == 0 && mep_index == 4471 && eep_index == 0 && sep_index == 5561 && center_index == 0) {
			if (brackets) {
				for (int sol : current_solution) {
					solution += move_names[sol];
					solution += " ";
				}
			}
			else {
				for (int i = 0; i < current_solution.size() - 2; ++i) {
					solution += move_names[current_solution[i]];
					solution += " ";
				}
				if (auf_adf.contains(current_solution[current_solution.size() - 2]) && auf_adf.contains(current_solution[current_solution.size() - 1])) {
					solution += "(";
					solution += move_names[current_solution[current_solution.size() - 2]];
					solution += " ";
					solution += move_names[current_solution[current_solution.size() - 1]];
					solution += ")";
				}
				else if (auf_adf.contains(current_solution[current_solution.size() - 1])) {
					solution += move_names[current_solution[current_solution.size() - 2]];
					solution += " (";
					solution += move_names[current_solution[current_solution.size() - 1]];
					solution += ")";
				}
				else {
					solution += move_names[current_solution[current_solution.size() - 2]];
					solution += " ";
					solution += move_names[current_solution[current_solution.size() - 1]];
				}
			}
			++count;
			if (count > solutions) {
				exit(0);
			}
			std::cout << solution << std::endl;
			solution = "";

			return true;
		}

		if (depth == 0) {
			return false;
		}

		if (std::max({ (((co_index * 40320 + cp_index) % 2 == 0) ? (co_cp_prune_table_E[(co_index * 40320 + cp_index) / 2] >> 4) : (co_cp_prune_table_E[(co_index * 40320 + cp_index) / 2] & 0b00001111)),
						(((cp_index * 11880 + mep_index) % 2 == 0) ? (cp_mep_prune_table_E[(cp_index * 11880 + mep_index) / 2] >> 4) : (cp_mep_prune_table_E[(cp_index * 11880 + mep_index) / 2] & 0b00001111)),
						(((co_index * 2048 * 24 + eo_index * 24 + center_index) % 2 == 0) ? (co_eo_center_prune_table_E[(co_index * 2048 * 24 + eo_index * 24 + center_index) / 2] >> 4) : (co_eo_center_prune_table_E[(co_index * 2048 * 24 + eo_index * 24 + center_index) / 2] & 0b00001111)) }) > depth) {
            return false;
		}

		int prev_move;
		if (!(current_solution.empty())) {
			prev_move = current_solution.back();
		}
		else {
			prev_move = -1;
		}

		for (int move_num : move_name_index_E) {
			if (prev_move == -1) {
				if (move_num == forbidden || move_num == (forbidden + 1) || move_num == (forbidden + 2) || move_num == (forbidden + 18) || move_num == (forbidden + 19) || move_num == (forbidden + 20)) {
					continue;
				}
				else {
					goto PASS;
				}
			}
			if (!(is_move_available[prev_move][move_num])) {
				continue;
			}
		PASS:

			current_solution.push_back(move_num);
			next_co_index = co_move_table_E[co_index][move_num];
			next_eo_index = eo_move_table_E[eo_index][move_num];
			next_cp_index = cp_move_table_E[cp_index][move_num];
			next_mep_index = ep_move_table_E[mep_index][move_num];
			next_eep_index = ep_move_table_E[eep_index][move_num];
			next_sep_index = ep_move_table_E[sep_index][move_num];
			next_center_index = center_move_table_E[center_index][move_num];
			limited_search_PLL_fs(next_co_index, next_eo_index, next_cp_index, next_mep_index, next_eep_index, next_sep_index, next_center_index, depth - 1);
			current_solution.pop_back();
		}
		return false;
	}

	void start_search_fs(int min_length, int max_length, int sol_num) {
		max_solution_length = max_length;
		solutions = sol_num;
		int co_index = co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int cp_index = cp_to_index(initial_state.cp);
		int mep_index = MEP_to_index(initial_state.ep);
		int eep_index = EEP_to_index(initial_state.ep);
		int sep_index = SEP_to_index(initial_state.ep);
		int center_index = center_to_index(initial_state.center);
		int min_depth = min_length;
		if (pattern == 0) {
			move_names = x_rotation_move_names;
		}

		while (min_depth <= max_solution_length) {
			std::cout << "\nstart searching in depth" << min_depth << "\n" << std::endl;
			if (limited_search_PLL_fs(co_index, eo_index, cp_index, mep_index, eep_index, sep_index, center_index, min_depth)) {
				;
			}
			++min_depth;
		}
		return;
	}

};

struct Search_PLL3 {

	State_fs initial_state;

	int max_solution_length;
	int solutions;
	int count = 0;

	std::vector<int> current_solution;
	int next_co_index;
	int next_eo_index;
	int next_cp_index;
	int next_mep_index;
	int next_eep_index;
	int next_sep_index;
	int next_center_index;

	bool found;

	std::unordered_map<int, int> inv = { { 0, 3 }, { 12, 15 }, { 15, 12 } };
	std::set<int> auf_adf = { forbidden, forbidden + 2, inv[forbidden], inv[forbidden] + 2 };

	std::string solution;

	std::vector<std::string> move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'",
											"R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" ,
											"Uw", "Uw2", "Uw'", "Dw", "Dw2", "Dw'", "Lw", "Lw2", "Lw'",
											"Rw", "Rw2", "Rw'", "Fw", "Fw2", "Fw'", "Bw", "Bw2", "Bw'",
											"M", "M2", "M'", "E", "E2", "E'", "S", "S2", "S'" };
	Search_PLL3(State_fs arg_state) {
		initial_state = arg_state;
	}

	bool limited_search_PLL_fs(int co_index, int eo_index, int cp_index, int mep_index, int eep_index, int sep_index, int center_index, int depth) {
		found = false;
		if (depth == 0 && co_index == 0 && eo_index == 0 && cp_index == 0 && mep_index == 4471 && eep_index == 0 && sep_index == 5561 && center_index == 0) {
			if (brackets) {
				for (int sol : current_solution) {
					solution += move_names[sol];
					solution += " ";
				}
			}
			else {
				for (int i = 0; i < current_solution.size() - 2; ++i) {
					solution += move_names[current_solution[i]];
					solution += " ";
				}
				if (auf_adf.contains(current_solution[current_solution.size() - 2]) && auf_adf.contains(current_solution[current_solution.size() - 1])) {
					solution += "(";
					solution += move_names[current_solution[current_solution.size() - 2]];
					solution += " ";
					solution += move_names[current_solution[current_solution.size() - 1]];
					solution += ")";
				}
				else if (auf_adf.contains(current_solution[current_solution.size() - 1])) {
					solution += move_names[current_solution[current_solution.size() - 2]];
					solution += " (";
					solution += move_names[current_solution[current_solution.size() - 1]];
					solution += ")";
				}
				else {
					solution += move_names[current_solution[current_solution.size() - 2]];
					solution += " ";
					solution += move_names[current_solution[current_solution.size() - 1]];
				}
			}

			++count;
			if (count > solutions) {
				exit(0);
			}
			std::cout << solution << std::endl;
			solution = "";

			return true;
		}

		if (depth == 0) {
			return false;
		}

		if (std::max({ (((co_index * 40320 + cp_index) % 2 == 0) ? (co_cp_prune_table_E[(co_index * 40320 + cp_index) / 2] >> 4) : (co_cp_prune_table_E[(co_index * 40320 + cp_index) / 2] & 0b00001111)),
				(((co_index * 2048 * 24 + eo_index * 24 + center_index) % 2 == 0) ? (co_eo_center_prune_table_E[(co_index * 2048 * 24 + eo_index * 24 + center_index) / 2] >> 4) : (co_eo_center_prune_table_E[(co_index * 2048 * 24 + eo_index * 24 + center_index) / 2] & 0b00001111)) }) > depth) {
			return false;
		}

		int prev_move;
		if (!(current_solution.empty())) {
			prev_move = current_solution.back();
		}
		else {
			prev_move = -1;
		}

		for (int move_num : move_name_index_E) {
			if (prev_move == -1) {
				if (move_num == forbidden ||  move_num == (forbidden + 2) || move_num == (forbidden + 18) || move_num == (forbidden + 20)) {
					continue;
				}
				else {
					goto PASS;
				}
			}
			if (!(is_move_available[prev_move][move_num])) {
				continue;
			}
		PASS:

			current_solution.push_back(move_num);
			next_co_index = co_move_table_E[co_index][move_num];
			next_eo_index = eo_move_table_E[eo_index][move_num];
			next_cp_index = cp_move_table_E[cp_index][move_num];
			next_mep_index = ep_move_table_E[mep_index][move_num];
			next_eep_index = ep_move_table_E[eep_index][move_num];
			next_sep_index = ep_move_table_E[sep_index][move_num];
			next_center_index = center_move_table_E[center_index][move_num];
			limited_search_PLL_fs(next_co_index, next_eo_index, next_cp_index, next_mep_index, next_eep_index, next_sep_index, next_center_index, depth - 1);
			current_solution.pop_back();
		}
		return false;
	}

	void start_search_fs(int min_length, int max_length, int sol_num) {
		max_solution_length = max_length;
		solutions = sol_num;
		int co_index = co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int cp_index = cp_to_index(initial_state.cp);
		int mep_index = MEP_to_index(initial_state.ep);
		int eep_index = EEP_to_index(initial_state.ep);
		int sep_index = SEP_to_index(initial_state.ep);
		int center_index = center_to_index(initial_state.center);
		int min_depth = min_length;
		if (pattern == 0) {
			move_names = x_rotation_move_names;
		}

		while (min_depth <= max_solution_length) {
			std::cout << "\nstart searching in depth" << min_depth << "\n" << std::endl;
			if (limited_search_PLL_fs(co_index, eo_index, cp_index, mep_index, eep_index, sep_index, center_index, min_depth)) {
				;
			}
			++min_depth;
		}
		return;
	}

};

struct Search_OLL0 {

	State initial_state;

	int max_solution_length;
	int solutions;
	int count = 0;

	std::vector<int> current_solution;
	int next_co_index;
	int next_eo_index;
	int next_cp_index;
	int next_mep_index;
	int next_eep_index;
	int next_sep_index;

	bool found;

	std::unordered_map<int, int> inv = { { 0, 3 }, { 12, 15 }, { 15, 12 } };
	std::set<int> adf = { inv[forbidden], inv[forbidden] + 1, inv[forbidden] + 2 };

	std::string solution;

	Search_OLL0(State arg_state) {
		initial_state = arg_state;
	}

	bool limited_search_OLL(int co_index, int eo_index, int cp_index, int mep_index, int eep_index, int sep_index, int depth) {
		found = false;
		if (co_index == 0 && eo_index == 0 && cp_index == 0 && meplist.contains(mep_index) && eep_index == 0 && seplist.contains(sep_index)) {
			if (depth != 0) {
				return false;
			}

			if (brackets) {
				for (int sol : current_solution) {
					solution += x_rotation_move_names[sol];
					solution += " ";
				}
			}

			else {
				for (int i = 0; i < current_solution.size() - 1; ++i) {
					solution += x_rotation_move_names[current_solution[i]];
					solution += " ";
				}

				if (adf.contains(current_solution[current_solution.size() - 1])) {
					solution += "(";
					solution += x_rotation_move_names[current_solution[current_solution.size() - 1]];
					solution += ")";
				}

				else {
					solution += x_rotation_move_names[current_solution[current_solution.size() - 1]];
				}
			}
			++count;
			if (count > solutions) {
				exit(0);
			}
			std::cout << solution << std::endl;
			solution = "";

			return true;
		}

		if (depth == 0) {
			return false;
		}

		if (std::max({ (((co_index * 1680 + cp_index) % 2 == 0) ? (co_cp_prune_table_E[(co_index * 1680 + cp_index) / 2] >> 4) : (co_cp_prune_table_E[(co_index * 1680 + cp_index) / 2] & 0b00001111)),
						(((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
						(((co_index * 2048 + eo_index) % 2 == 0) ? (co_eo_prune_table_E[(co_index * 2048 + eo_index) / 2] >> 4) : (co_eo_prune_table_E[(co_index * 2048 + eo_index) / 2] & 0b00001111)),
						(((eo_index * 11880 + eep_index) % 2 == 0) ? (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] >> 4) : (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] & 0b00001111)) }) > depth) {
			return false;
		}
		int prev_move;
		if (!(current_solution.empty())) {
			prev_move = current_solution.back();
		}
		else {
			prev_move = -1;
		}

		for (int move_num : move_name_index_E) {
			if (prev_move == -1) {
				if (move_num == forbidden || move_num == (forbidden + 1) || move_num == (forbidden + 2)) {
					continue;
				}
				else {
					goto PASS;
				}
			}
			if (!(is_move_available[prev_move][move_num])) {
				continue;
			}
		PASS:
			current_solution.push_back(move_num);
			next_co_index = co_move_table_E[co_index][move_num];
			next_eo_index = eo_move_table_E[eo_index][move_num];
			next_cp_index = cp_move_table_E[cp_index][move_num];
			next_mep_index = ep_move_table_E[mep_index][move_num];
			next_eep_index = ep_move_table_E[eep_index][move_num];
			next_sep_index = ep_move_table_E[sep_index][move_num];
			limited_search_OLL(next_co_index, next_eo_index, next_cp_index, next_mep_index, next_eep_index, next_sep_index, depth - 1);
			current_solution.pop_back();
		}
		return false;
	}

	void start_search(int min_length, int max_length, int sol_num) {
		max_solution_length = max_length;
		solutions = sol_num;
		int co_index = co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int cp_index = OLL_cp_to_index(initial_state.cp);
		int mep_index = MEP_to_index(initial_state.ep);
		int eep_index = EEP_to_index(initial_state.ep);
		int sep_index = SEP_to_index(initial_state.ep);
		int min_depth = min_length;

		while (min_depth <= max_solution_length) {
			std::cout << "\nstart searching in depth" << min_depth << "\n" << std::endl;
			if (limited_search_OLL(co_index, eo_index, cp_index, mep_index, eep_index, sep_index, min_depth)) {
				;
			}
			++min_depth;
		}
		return;
	}
};

struct Search_OLL1 {

	State initial_state;

	int max_solution_length;
	int solutions;
	int count = 0;

	std::vector<int> current_solution;
	int next_co_index;
	int next_eo_index;
	int next_cp_index;
	int next_mep_index;
	int next_eep_index;
	int next_sep_index;

	bool found;

	std::unordered_map<int, int> inv = { { 0, 3 }, { 12, 15 }, { 15, 12 } };
	std::set<int> adf = { inv[forbidden], inv[forbidden] + 1, inv[forbidden] + 2 };

	std::string solution;

	Search_OLL1(State arg_state) {
		initial_state = arg_state;
	}

	bool limited_search_OLL(int co_index, int eo_index, int cp_index, int mep_index, int eep_index, int sep_index, int depth) {
		found = false;
		if (co_index == 0 && eo_index == 0 && cp_index == 0 && meplist.contains(mep_index) && eep_index == 0 && seplist.contains(sep_index)) {
			if (depth != 0) {
				return false;
			}

			if (brackets) {
				for (int sol : current_solution) {
					solution += x_rotation_move_names[sol];
					solution += " ";
				}
			}

			else {
				for (int i = 0; i < current_solution.size() - 1; ++i) {
					solution += x_rotation_move_names[current_solution[i]];
					solution += " ";
				}

				if (adf.contains(current_solution[current_solution.size() - 1])) {
					solution += "(";
					solution += x_rotation_move_names[current_solution[current_solution.size() - 1]];
					solution += ")";
				}

				else {
					solution += x_rotation_move_names[current_solution[current_solution.size() - 1]];
				}
			}
			++count;
			if (count > solutions) {
				exit(0);
			}
			std::cout << solution << std::endl;
			solution = "";

			return true;
		}

		if (depth == 0) {
			return false;
		}

		if (std::max({ (((co_index * 1680 + cp_index) % 2 == 0) ? (co_cp_prune_table_E[(co_index * 1680 + cp_index) / 2] >> 4) : (co_cp_prune_table_E[(co_index * 1680 + cp_index) / 2] & 0b00001111)),
						(((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
						(((co_index * 2048 + eo_index) % 2 == 0) ? (co_eo_prune_table_E[(co_index * 2048 + eo_index) / 2] >> 4) : (co_eo_prune_table_E[(co_index * 2048 + eo_index) / 2] & 0b00001111)),
						(((eo_index * 11880 + eep_index) % 2 == 0) ? (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] >> 4) : (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] & 0b00001111)) }) > depth) {
			return false;
		}
		int prev_move;
		if (!(current_solution.empty())) {
			prev_move = current_solution.back();
		}
		else {
			prev_move = -1;
		}

		for (int move_num : move_name_index_E) {
			if (prev_move == -1) {
				if (move_num == forbidden || move_num == (forbidden + 2)) {
					continue;
				}
				else {
					goto PASS;
				}
			}
			if (!(is_move_available[prev_move][move_num])) {
				continue;
			}
		PASS:
			current_solution.push_back(move_num);
			next_co_index = co_move_table_E[co_index][move_num];
			next_eo_index = eo_move_table_E[eo_index][move_num];
			next_cp_index = cp_move_table_E[cp_index][move_num];
			next_mep_index = ep_move_table_E[mep_index][move_num];
			next_eep_index = ep_move_table_E[eep_index][move_num];
			next_sep_index = ep_move_table_E[sep_index][move_num];
			limited_search_OLL(next_co_index, next_eo_index, next_cp_index, next_mep_index, next_eep_index, next_sep_index, depth - 1);
			current_solution.pop_back();
		}
		return false;
	}

	void start_search(int min_length, int max_length, int sol_num) {
		max_solution_length = max_length;
		solutions = sol_num;
		int co_index = co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int cp_index = OLL_cp_to_index(initial_state.cp);
		int mep_index = MEP_to_index(initial_state.ep);
		int eep_index = EEP_to_index(initial_state.ep);
		int sep_index = SEP_to_index(initial_state.ep);
		int min_depth = min_length;

		while (min_depth <= max_solution_length) {
			std::cout << "\nstart searching in depth" << min_depth << "\n" << std::endl;
			if (limited_search_OLL(co_index, eo_index, cp_index, mep_index, eep_index, sep_index, min_depth)) {
				;
			}
			++min_depth;
		}
		return;
	}
};

struct Search_OLL2 {

	State_fs initial_state;

	int max_solution_length;
	int solutions;
	int count = 0;

	std::vector<int> current_solution;
	int next_co_index;
	int next_eo_index;
	int next_cp_index;
	int next_mep_index;
	int next_eep_index;
	int next_sep_index;
	int next_center_index;

	bool found;

	std::unordered_map<int, int> inv = { { 0, 3 }, { 12, 15 }, { 15, 12 } };
	std::set<int> adf = { inv[forbidden], inv[forbidden] + 1, inv[forbidden] + 2 };

	std::string solution;

	Search_OLL2(State_fs arg_state) {
		initial_state = arg_state;
	}

	bool limited_search_OLL_fs(int co_index, int eo_index, int cp_index, int mep_index, int eep_index, int sep_index, int center_index, int depth) {
		found = false;
		if (co_index == 0 && eo_index == 0 && cp_index == 0 && meplist.contains(mep_index) && eep_index == 0 && seplist.contains(sep_index) && center_index == 0) {
			if (depth != 0) {
				return false;
			}

			if (brackets) {
				for (int sol : current_solution) {
					solution += x_rotation_move_names[sol];
					solution += " ";
				}
			}

			else {
				for (int i = 0; i < current_solution.size() - 1; ++i) {
					solution += x_rotation_move_names[current_solution[i]];
					solution += " ";
				}

				if (adf.contains(current_solution[current_solution.size() - 1])) {
					solution += "(";
					solution += x_rotation_move_names[current_solution[current_solution.size() - 1]];
					solution += ")";
				}

				else {
					solution += x_rotation_move_names[current_solution[current_solution.size() - 1]];
				}
			}
			++count;
			if (count > solutions) {
				exit(0);
			}
			std::cout << solution << std::endl;
			solution = "";

			return true;
		}

		if (depth == 0) {
			return false;
		}

		if (std::max({ (((co_index * 1680 + cp_index) % 2 == 0) ? (co_cp_prune_table_E[(co_index * 1680 + cp_index) / 2] >> 4) : (co_cp_prune_table_E[(co_index * 1680 + cp_index) / 2] & 0b00001111)),
						(((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
						(((eo_index * 11880 + eep_index) % 2 == 0) ? (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] >> 4) : (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] & 0b00001111)),
						(((co_index * 2048 * 24 + eo_index * 24 + center_index) % 2 == 0) ? (co_eo_center_prune_table_E[(co_index * 2048 * 24 + eo_index * 24 + center_index) / 2] >> 4) : (co_eo_center_prune_table_E[(co_index * 2048 * 24 + eo_index * 24 + center_index) / 2] & 0b00001111)),
						(((cp_index * 11880 * 24 + eep_index * 24 + center_index) % 2 == 0) ? (cp_eep_center_prune_table_E[(cp_index * 11880 * 24 + eep_index * 24 + center_index) / 2] >> 4) : (cp_eep_center_prune_table_E[(cp_index * 11880 * 24 + eep_index * 24 + center_index) / 2] & 0b00001111)) }) > depth) {
			return false;
		}
		int prev_move;
		if (!(current_solution.empty())) {
			prev_move = current_solution.back();
		}
		else {
			prev_move = -1;
		}

		for (int move_num : move_name_index_E) {
			if (prev_move == -1) {
				if (move_num == forbidden || move_num == (forbidden + 1) || move_num == (forbidden + 2) || move_num == (forbidden + 18) || move_num == (forbidden + 19) || move_num == (forbidden + 20)) {
					continue;
				}
				else {
					goto PASS;
				}
			}
			if (!(is_move_available[prev_move][move_num])) {
				continue;
			}
		PASS:
			current_solution.push_back(move_num);
			next_co_index = co_move_table_E[co_index][move_num];
			next_eo_index = eo_move_table_E[eo_index][move_num];
			next_cp_index = cp_move_table_E[cp_index][move_num];
			next_mep_index = ep_move_table_E[mep_index][move_num];
			next_eep_index = ep_move_table_E[eep_index][move_num];
			next_sep_index = ep_move_table_E[sep_index][move_num];
			next_center_index = center_move_table_E[center_index][move_num];
			limited_search_OLL_fs(next_co_index, next_eo_index, next_cp_index, next_mep_index, next_eep_index, next_sep_index, next_center_index, depth - 1);
			current_solution.pop_back();
		}
		return false;
	}

	void start_search_fs(int min_length, int max_length, int sol_num) {
		max_solution_length = max_length;
		solutions = sol_num;
		int co_index = co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int cp_index = OLL_cp_to_index(initial_state.cp);
		int mep_index = MEP_to_index(initial_state.ep);
		int eep_index = EEP_to_index(initial_state.ep);
		int sep_index = SEP_to_index(initial_state.ep);
		int center_index = center_to_index(initial_state.center);
		int min_depth = min_length;

		while (min_depth <= max_solution_length) {
			std::cout << "\nstart searching in depth" << min_depth << "\n" << std::endl;
			if (limited_search_OLL_fs(co_index, eo_index, cp_index, mep_index, eep_index, sep_index, center_index, min_depth)) {
				;
			}
			++min_depth;
		}
		return;
	}
};

struct Search_OLL3 {

	State_fs initial_state;

	int max_solution_length;
	int solutions;
	int count = 0;

	std::vector<int> current_solution;
	int next_co_index;
	int next_eo_index;
	int next_cp_index;
	int next_mep_index;
	int next_eep_index;
	int next_sep_index;
	int next_center_index;

	bool found;

	std::unordered_map<int, int> inv = { { 0, 3 }, { 12, 15 }, { 15, 12 } };
	std::set<int> adf = { inv[forbidden], inv[forbidden] + 2 };

	std::string solution;

	Search_OLL3(State_fs arg_state) {
		initial_state = arg_state;
	}

	bool limited_search_OLL_fs(int co_index, int eo_index, int cp_index, int mep_index, int eep_index, int sep_index, int center_index, int depth) {
		found = false;
		if (co_index == 0 && eo_index == 0 && cp_index == 0 && meplist.contains(mep_index) && eep_index == 0 && seplist.contains(sep_index) && center_index == 0) {
			if (depth != 0) {
				return false;
			}

			if (brackets) {
				for (int sol : current_solution) {
					solution += x_rotation_move_names[sol];
					solution += " ";
				}
			}

			else {
				for (int i = 0; i < current_solution.size() - 1; ++i) {
					solution += x_rotation_move_names[current_solution[i]];
					solution += " ";
				}

				if (adf.contains(current_solution[current_solution.size() - 1])) {
					solution += "(";
					solution += x_rotation_move_names[current_solution[current_solution.size() - 1]];
					solution += ")";
				}

				else {
					solution += x_rotation_move_names[current_solution[current_solution.size() - 1]];
				}
			}
			++count;
			if (count > solutions) {
				exit(0);
			}
			std::cout << solution << std::endl;
			solution = "";

			return true;
		}

		if (depth == 0) {
			return false;
		}

		if (std::max({ (((co_index * 1680 + cp_index) % 2 == 0) ? (co_cp_prune_table_E[(co_index * 1680 + cp_index) / 2] >> 4) : (co_cp_prune_table_E[(co_index * 1680 + cp_index) / 2] & 0b00001111)),
						(((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
						(((cp_index * 11880 + eep_index) % 2 == 0) ? (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] >> 4) : (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] & 0b00001111)),
						(((co_index * 2048 * 24 + eo_index * 24 + center_index) % 2 == 0) ? (co_eo_center_prune_table_E[(co_index * 2048 * 24 + eo_index * 24 + center_index) / 2] >> 4) : (co_eo_center_prune_table_E[(co_index * 2048 * 24 + eo_index * 24 + center_index) / 2] & 0b00001111)) }) > depth) {
			return false;
		}
		int prev_move;
		if (!(current_solution.empty())) {
			prev_move = current_solution.back();
		}
		else {
			prev_move = -1;
		}

		for (int move_num : move_name_index_E) {
			if (prev_move == -1) {
				if (move_num == forbidden || move_num == (forbidden + 2) || move_num == (forbidden + 18) || move_num == (forbidden + 20)) {
					continue;
				}
				else {
					goto PASS;
				}
			}
			if (!(is_move_available[prev_move][move_num])) {
				continue;
			}
		PASS:
			current_solution.push_back(move_num);
			next_co_index = co_move_table_E[co_index][move_num];
			next_eo_index = eo_move_table_E[eo_index][move_num];
			next_cp_index = cp_move_table_E[cp_index][move_num];
			next_mep_index = ep_move_table_E[mep_index][move_num];
			next_eep_index = ep_move_table_E[eep_index][move_num];
			next_sep_index = ep_move_table_E[sep_index][move_num];
			next_center_index = center_move_table_E[center_index][move_num];
			limited_search_OLL_fs(next_co_index, next_eo_index, next_cp_index, next_mep_index, next_eep_index, next_sep_index, next_center_index, depth - 1);
			current_solution.pop_back();
		}
		return false;
	}

	void start_search_fs(int min_length, int max_length, int sol_num) {
		max_solution_length = max_length;
		solutions = sol_num;
		int co_index = co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int cp_index = OLL_cp_to_index(initial_state.cp);
		int mep_index = MEP_to_index(initial_state.ep);
		int eep_index = EEP_to_index(initial_state.ep);
		int sep_index = SEP_to_index(initial_state.ep);
		int center_index = center_to_index(initial_state.center);
		int min_depth = min_length;

		while (min_depth <= max_solution_length) {
			std::cout << "\nstart searching in depth" << min_depth << "\n" << std::endl;
			if (limited_search_OLL_fs(co_index, eo_index, cp_index, mep_index, eep_index, sep_index, center_index, min_depth)) {
				;
			}
			++min_depth;
		}
		return;
	}
};

struct Search_F2L0 {

	State initial_state;

	int max_solution_length;
	int solutions;
	int count = 0;

	std::vector<int> current_solution;
	int next_co_index;
	int next_eo_index;
	int next_cp_index;
	int next_mep_index;
	int next_eep_index;
	int next_sep_index;

	bool found;

	std::string solution;
	
	std::vector<std::string> move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'",
										"R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" };

	Search_F2L0(State arg_state) {
		initial_state = arg_state;
	}

	bool limited_search_F2L(int co_index, int eo_index, int cp_index, int mep_index, int eep_index, int sep_index, int depth) {
		found = false;
		if (co_index == solved_co && solved_eo.contains(eo_index) && cp_index == solved_cp && solved_mep.contains(mep_index) && solved_eep.contains(eep_index) && solved_sep.contains(sep_index)) {
			if (depth != 0) {
				return false;
			}

			for (int sol : current_solution) {
				solution += move_names[sol];
				solution += " ";
			}

			++count;
			if (count > solutions) {
				exit(0);
			}
			std::cout << solution << std::endl;
			solution = "";

			return true;
		}

		if (depth == 0) {
			return false;
		}

		if (pattern == 0) {
			if (std::max({ (((mep_index * 11880 + sep_index) % 2 == 0) ? (mep_sep_prune_table_E[(mep_index * 11880 + sep_index) / 2] >> 4) : (mep_sep_prune_table_E[(mep_index * 11880 + sep_index) / 2] & 0b00001111)),
							(((eo_index * 11880 + mep_index) % 2 == 0) ? (eo_mep_prune_table_E[(eo_index * 11880 + mep_index) / 2] >> 4) : (eo_mep_prune_table_E[(eo_index * 11880 + mep_index) / 2] & 0b00001111)),
							(((eo_index * 11880 + sep_index) % 2 == 0) ? (eo_sep_prune_table_E[(eo_index * 11880 + sep_index) / 2] >> 4) : (eo_sep_prune_table_E[(eo_index * 11880 + sep_index) / 2] & 0b00001111)) }) > depth) {
				return false;
			}
		}
		
		else if (pattern == 1) {
			if (std::max({ (((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + sep_index) % 2 == 0) ? (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] >> 4) : (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + mep_index) % 2 == 0) ? (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] >> 4) : (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] & 0b00001111)),
							(((eo_index * 11880 + eep_index) % 2 == 0) ? (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] >> 4) : (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] & 0b00001111)) }) > depth) {
				return false;
			}
		}
		
		else if (pattern == 2) {
			if (std::max({ (((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + sep_index) % 2 == 0) ? (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] >> 4) : (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + mep_index) % 2 == 0) ? (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] >> 4) : (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] & 0b00001111)),
							(((eo_index * 11880 + eep_index) % 2 == 0) ? (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] >> 4) : (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] & 0b00001111)) }) > depth) {
				return false;
			}
		}
		
		else if (pattern == 3) {
			if (std::max({ (((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + sep_index) % 2 == 0) ? (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] >> 4) : (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + mep_index) % 2 == 0) ? (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] >> 4) : (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] & 0b00001111)),
							(((eo_index * 11880 + eep_index) % 2 == 0) ? (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] >> 4) : (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] & 0b00001111)),
							(((cp_index * 11880 + eep_index) % 2 == 0) ? (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] >> 4) : (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] & 0b00001111)) }) > depth) {
				return false;
			}
		}

		int prev_move;
		if (!(current_solution.empty())) {
			prev_move = current_solution.back();
		}
		else {
			prev_move = -1;
		}

		for (int move_num : move_name_index_E) {
			if (prev_move == -1) {
				if (move_num == 0 || move_num == 1 || move_num == 2) {
					continue;
				}
				else {
					goto PASS;
				}
			}
			if (!(is_move_available[prev_move][move_num])) {
				continue;
			}
		PASS:
			current_solution.push_back(move_num);
			next_co_index = co_move_table_E[co_index][move_num];
			next_eo_index = eo_move_table_E[eo_index][move_num];
			next_cp_index = cp_move_table_E[cp_index][move_num];
			next_mep_index = ep_move_table_E[mep_index][move_num];
			next_eep_index = ep_move_table_E[eep_index][move_num];
			next_sep_index = ep_move_table_E[sep_index][move_num];
			limited_search_F2L(next_co_index, next_eo_index, next_cp_index, next_mep_index, next_eep_index, next_sep_index, depth - 1);
			current_solution.pop_back();
		}
		return false;
	}

	void start_search(int min_length, int max_length, int sol_num) {
		max_solution_length = max_length;
		solutions = sol_num;
		int co_index = F2L_co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int cp_index = F2L_cp_to_index(initial_state.cp);
		int mep_index = MEP_to_index(initial_state.ep);
		int eep_index = EEP_to_index(initial_state.ep);
		int sep_index = SEP_to_index(initial_state.ep);
		int min_depth = min_length;
		while (min_depth <= max_solution_length) {
			std::cout << "\nstart searching in depth" << min_depth << "\n" << std::endl;
			if (limited_search_F2L(co_index, eo_index, cp_index, mep_index, eep_index, sep_index, min_depth)) {
				;
			}
			++min_depth;
		}
		return;
	}
};

struct Search_F2L1 {

	State initial_state;

	int max_solution_length;
	int solutions;
	int count = 0;

	std::vector<int> current_solution;
	int next_co_index;
	int next_eo_index;
	int next_cp_index;
	int next_mep_index;
	int next_eep_index;
	int next_sep_index;

	bool found;

	std::string solution;

	std::vector<std::string> move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'",
										"R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" };

	Search_F2L1(State arg_state) {
		initial_state = arg_state;
	}

	bool limited_search_F2L(int co_index, int eo_index, int cp_index, int mep_index, int eep_index, int sep_index, int depth) {
		found = false;
		if (co_index == solved_co && solved_eo.contains(eo_index) && cp_index == solved_cp && solved_mep.contains(mep_index) && solved_eep.contains(eep_index) && solved_sep.contains(sep_index)) {
			if (depth != 0) {
				return false;
			}

			for (int sol : current_solution) {
				solution += move_names[sol];
				solution += " ";
			}

			++count;
			if (count > solutions) {
				exit(0);
			}
			std::cout << solution << std::endl;
			solution = "";

			return true;
		}

		if (depth == 0) {
			return false;
		}

		if (pattern == 0) {
			if (std::max({ (((eo_index * 11880 + mep_index) % 2 == 0) ? (eo_mep_prune_table_E[(eo_index * 11880 + mep_index) / 2] >> 4) : (eo_mep_prune_table_E[(eo_index * 11880 + mep_index) / 2] & 0b00001111)),
							(((eo_index * 11880 + sep_index) % 2 == 0) ? (eo_sep_prune_table_E[(eo_index * 11880 + sep_index) / 2] >> 4) : (eo_sep_prune_table_E[(eo_index * 11880 + sep_index) / 2] & 0b00001111)) }) > depth) {
				return false;
			}
		}

		else if (pattern == 1) {
			if (std::max({ (((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + sep_index) % 2 == 0) ? (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] >> 4) : (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + mep_index) % 2 == 0) ? (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] >> 4) : (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] & 0b00001111)) }) > depth) {
				return false;
			}
		}

		else if (pattern == 2) {
			if (std::max({ (((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + sep_index) % 2 == 0) ? (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] >> 4) : (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + mep_index) % 2 == 0) ? (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] >> 4) : (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] & 0b00001111)),
							(((eo_index * 11880 + eep_index) % 2 == 0) ? (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] >> 4) : (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] & 0b00001111)),
							(((cp_index * 11880 + eep_index) % 2 == 0) ? (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] >> 4) : (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] & 0b00001111)) }) > depth) {
				return false;
			}
		}

		else if (pattern == 3) {
			if (std::max({ (((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + sep_index) % 2 == 0) ? (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] >> 4) : (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + mep_index) % 2 == 0) ? (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] >> 4) : (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] & 0b00001111)),
							(((eo_index * 11880 + eep_index) % 2 == 0) ? (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] >> 4) : (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] & 0b00001111)),
							(((cp_index * 11880 + eep_index) % 2 == 0) ? (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] >> 4) : (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] & 0b00001111)) }) > depth) {
				return false;
			}
		}

		int prev_move;
		if (!(current_solution.empty())) {
			prev_move = current_solution.back();
		}
		else {
			prev_move = -1;
		}

		for (int move_num : move_name_index_E) {
			if (prev_move == -1) {
				if (move_num == 0 || move_num == 2) {
					continue;
				}
				else {
					goto PASS;
				}
			}
			if (!(is_move_available[prev_move][move_num])) {
				continue;
			}
		PASS:
			current_solution.push_back(move_num);
			next_co_index = co_move_table_E[co_index][move_num];
			next_eo_index = eo_move_table_E[eo_index][move_num];
			next_cp_index = cp_move_table_E[cp_index][move_num];
			next_mep_index = ep_move_table_E[mep_index][move_num];
			next_eep_index = ep_move_table_E[eep_index][move_num];
			next_sep_index = ep_move_table_E[sep_index][move_num];
			limited_search_F2L(next_co_index, next_eo_index, next_cp_index, next_mep_index, next_eep_index, next_sep_index, depth - 1);
			current_solution.pop_back();
		}
		return false;
	}

	void start_search(int min_length, int max_length, int sol_num) {
		max_solution_length = max_length;
		solutions = sol_num;
		int co_index = F2L_co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int cp_index = F2L_cp_to_index(initial_state.cp);
		int mep_index = MEP_to_index(initial_state.ep);
		int eep_index = EEP_to_index(initial_state.ep);
		int sep_index = SEP_to_index(initial_state.ep);
		int min_depth = min_length;

		while (min_depth <= max_solution_length) {
			std::cout << "\nstart searching in depth" << min_depth << "\n" << std::endl;
			if (limited_search_F2L(co_index, eo_index, cp_index, mep_index, eep_index, sep_index, min_depth)) {
				;
			}
			++min_depth;
		}
		return;
	}
};

struct Search_F2L2 {

	State_fs initial_state;

	int max_solution_length;
	int solutions;
	int count = 0;

	std::vector<int> current_solution;
	int next_co_index;
	int next_eo_index;
	int next_cp_index;
	int next_mep_index;
	int next_eep_index;
	int next_sep_index;
	int next_center_index;

	bool found;

	std::string solution;

	std::vector<std::string> move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'",
											"R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" ,
											"Uw", "Uw2", "Uw'", "Dw", "Dw2", "Dw'", "Lw", "Lw2", "Lw'",
											"Rw", "Rw2", "Rw'", "Fw", "Fw2", "Fw'", "Bw", "Bw2", "Bw'",
											"M", "M2", "M'", "E", "E2", "E'", "S", "S2", "S'" };

	Search_F2L2(State_fs arg_state) {
		initial_state = arg_state;
	}

	bool limited_search_F2L_fs(int co_index, int eo_index, int cp_index, int mep_index, int eep_index, int sep_index, int center_index, int depth) {
		found = false;
		if (co_index == solved_co && solved_eo.contains(eo_index) && cp_index == solved_cp && solved_mep.contains(mep_index) && solved_eep.contains(eep_index) && solved_sep.contains(sep_index) && center_index == 0) {
			if (depth != 0) {
				return false;
			}

			for (int sol : current_solution) {
				solution += move_names[sol];
				solution += " ";
			}

			++count;
			if (count > solutions) {
				exit(0);
			}
			std::cout << solution << std::endl;
			solution = "";

			return true;
		}

		if (depth == 0) {
			return false;
		}

		if (pattern == 0) {
			if (std::max({ (((co_index * 11880 + mep_index) % 2 == 0) ? (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] >> 4) : (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + sep_index) % 2 == 0) ? (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] >> 4) : (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] & 0b00001111)) }) > depth) {
				return false;
			}
		}

		else if (pattern == 1) {
			if (std::max({ (((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + sep_index) % 2 == 0) ? (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] >> 4) : (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + mep_index) % 2 == 0) ? (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] >> 4) : (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] & 0b00001111)) }) > depth) {
				return false;
			}
		}

		else if (pattern == 2) {
			if (std::max({ (((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + sep_index) % 2 == 0) ? (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] >> 4) : (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + mep_index) % 2 == 0) ? (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] >> 4) : (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] & 0b00001111)),
							(((cp_index * 11880 + eep_index) % 2 == 0) ? (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] >> 4) : (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] & 0b00001111)) }) > depth) {
				return false;
			}
		}

		else if (pattern == 3) {
			if (std::max({ (((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + sep_index) % 2 == 0) ? (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] >> 4) : (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + mep_index) % 2 == 0) ? (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] >> 4) : (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] & 0b00001111)),
							(((cp_index * 11880 + eep_index) % 2 == 0) ? (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] >> 4) : (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] & 0b00001111)) }) > depth) {
				return false;
			}
		}

		int prev_move;
		if (!(current_solution.empty())) {
			prev_move = current_solution.back();
		}
		else {
			prev_move = -1;
		}

		for (int move_num : move_name_index_E) {
			if (prev_move == -1) {
				if (move_num == 0 || move_num == 1 || move_num == 2 || move_num == 18 || move_num == 19 || move_num == 20) {
					continue;
				}
				else {
					goto PASS;
				}
			}
			if (!(is_move_available[prev_move][move_num])) {
				continue;
			}
		PASS:
			current_solution.push_back(move_num);
			next_co_index = co_move_table_E[co_index][move_num];
			next_eo_index = eo_move_table_E[eo_index][move_num];
			next_cp_index = cp_move_table_E[cp_index][move_num];
			next_mep_index = ep_move_table_E[mep_index][move_num];
			next_eep_index = ep_move_table_E[eep_index][move_num];
			next_sep_index = ep_move_table_E[sep_index][move_num];
			next_center_index = center_move_table_E[center_index][move_num];
			limited_search_F2L_fs(next_co_index, next_eo_index, next_cp_index, next_mep_index, next_eep_index, next_sep_index, next_center_index,  depth - 1);
			current_solution.pop_back();
		}
		return false;
	}

	void start_search_fs(int min_length, int max_length, int sol_num) {
		max_solution_length = max_length;
		solutions = sol_num;
		int co_index = F2L_co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int cp_index = F2L_cp_to_index(initial_state.cp);
		int mep_index = MEP_to_index(initial_state.ep);
		int eep_index = EEP_to_index(initial_state.ep);
		int sep_index = SEP_to_index(initial_state.ep);
		int center_index = center_to_index(initial_state.center);
		int min_depth = min_length;

		while (min_depth <= max_solution_length) {
			std::cout << "\nstart searching in depth" << min_depth << "\n" << std::endl;
			if (limited_search_F2L_fs(co_index, eo_index, cp_index, mep_index, eep_index, sep_index, center_index, min_depth)) {
				;
			}
			++min_depth;
		}
		return;
	}
};

struct Search_F2L3 {

	State_fs initial_state;

	int max_solution_length;
	int solutions;
	int count = 0;

	std::vector<int> current_solution;
	int next_co_index;
	int next_eo_index;
	int next_cp_index;
	int next_mep_index;
	int next_eep_index;
	int next_sep_index;
	int next_center_index;

	bool found;

	std::string solution;

	std::vector<std::string> move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'",
											"R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" ,
											"Uw", "Uw2", "Uw'", "Dw", "Dw2", "Dw'", "Lw", "Lw2", "Lw'",
											"Rw", "Rw2", "Rw'", "Fw", "Fw2", "Fw'", "Bw", "Bw2", "Bw'",
											"M", "M2", "M'", "E", "E2", "E'", "S", "S2", "S'" };

	Search_F2L3(State_fs arg_state) {
		initial_state = arg_state;
	}

	bool limited_search_F2L_fs(int co_index, int eo_index, int cp_index, int mep_index, int eep_index, int sep_index, int center_index, int depth) {
		found = false;
		if (co_index == solved_co && solved_eo.contains(eo_index) && cp_index == solved_cp && solved_mep.contains(mep_index) && solved_eep.contains(eep_index) && solved_sep.contains(sep_index) && center_index == 0) {
			if (depth != 0) {
				return false;
			}

			for (int sol : current_solution) {
				solution += move_names[sol];
				solution += " ";
			}

			++count;
			if (count > solutions) {
				exit(0);
			}
			std::cout << solution << std::endl;
			solution = "";

			return true;
		}

		if (depth == 0) {
			return false;
		}

		if (pattern == 0) {
			if (std::max({ (((co_index * 11880 + mep_index) % 2 == 0) ? (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] >> 4) : (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + sep_index) % 2 == 0) ? (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] >> 4) : (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] & 0b00001111)) }) > depth) {
				return false;
			}
		}

		else if (pattern == 1) {
			if (std::max({ (((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + sep_index) % 2 == 0) ? (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] >> 4) : (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + mep_index) % 2 == 0) ? (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] >> 4) : (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] & 0b00001111)) }) > depth) {
				return false;
			}
		}

		else if (pattern == 2) {
			if (std::max({ (((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + sep_index) % 2 == 0) ? (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] >> 4) : (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + mep_index) % 2 == 0) ? (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] >> 4) : (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] & 0b00001111)),
							(((cp_index * 11880 + eep_index) % 2 == 0) ? (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] >> 4) : (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] & 0b00001111)) }) > depth) {
				return false;
			}
		}

		else if (pattern == 3) {
			if (std::max({ (((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + sep_index) % 2 == 0) ? (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] >> 4) : (co_sep_prune_table_E[(co_index * 11880 + sep_index) / 2] & 0b00001111)),
							(((co_index * 11880 + mep_index) % 2 == 0) ? (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] >> 4) : (co_mep_prune_table_E[(co_index * 11880 + mep_index) / 2] & 0b00001111)),
							(((cp_index * 11880 + eep_index) % 2 == 0) ? (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] >> 4) : (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] & 0b00001111)) }) > depth) {
				return false;
			}
		}

		int prev_move;
		if (!(current_solution.empty())) {
			prev_move = current_solution.back();
		}
		else {
			prev_move = -1;
		}

		for (int move_num : move_name_index_E) {
			if (prev_move == -1) {
				if (move_num == 0 || move_num == 2 || move_num == 18 || move_num == 20) {
					continue;
				}
				else {
					goto PASS;
				}
			}
			if (!(is_move_available[prev_move][move_num])) {
				continue;
			}
		PASS:
			current_solution.push_back(move_num);
			next_co_index = co_move_table_E[co_index][move_num];
			next_eo_index = eo_move_table_E[eo_index][move_num];
			next_cp_index = cp_move_table_E[cp_index][move_num];
			next_mep_index = ep_move_table_E[mep_index][move_num];
			next_eep_index = ep_move_table_E[eep_index][move_num];
			next_sep_index = ep_move_table_E[sep_index][move_num];
			next_center_index = center_move_table_E[center_index][move_num];
			limited_search_F2L_fs(next_co_index, next_eo_index, next_cp_index, next_mep_index, next_eep_index, next_sep_index, next_center_index, depth - 1);
			current_solution.pop_back();
		}
		return false;
	}

	void start_search_fs(int min_length, int max_length, int sol_num) {
		max_solution_length = max_length;
		solutions = sol_num;
		int co_index = F2L_co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int cp_index = F2L_cp_to_index(initial_state.cp);
		int mep_index = MEP_to_index(initial_state.ep);
		int eep_index = EEP_to_index(initial_state.ep);
		int sep_index = SEP_to_index(initial_state.ep);
		int center_index = center_to_index(initial_state.center);
		int min_depth = min_length;

		while (min_depth <= max_solution_length) {
			std::cout << "\nstart searching in depth" << min_depth << "\n" << std::endl;
			if (limited_search_F2L_fs(co_index, eo_index, cp_index, mep_index, eep_index, sep_index, center_index, min_depth)) {
				;
			}
			++min_depth;
		}
		return;
	}
};

struct Search_COLL0 {

	State initial_state;

	int max_solution_length;
	int solutions;
	int count = 0;

	std::vector<int> current_solution;
	int next_co_index;
	int next_eo_index;
	int next_cp_index;
	int next_mep_index;
	int next_eep_index;
	int next_sep_index;

	bool found;

	std::unordered_map<int, int> inv = { { 0, 3 }, { 12, 15 }, { 15, 12 } };
	std::set<int> auf_adf = { forbidden, forbidden + 1, forbidden + 2, inv[forbidden], inv[forbidden] + 1, inv[forbidden] + 2 };

	std::string solution;

	Search_COLL0(State arg_state) {
		initial_state = arg_state;
	}

	bool limited_search_COLL(int co_index, int eo_index, int cp_index, int mep_index, int eep_index, int sep_index, int depth) {
		found = false;
		if (co_index == 0 && eo_index == 0 && cp_index == 0 && meplist.contains(mep_index) && eep_index == 0 && seplist.contains(sep_index)) {
			if (depth != 0) {
				return false;
			}

			if (brackets) {
				for (int sol : current_solution) {
					solution += x_rotation_move_names[sol];
					solution += " ";
				}
			}
			else {
				for (int i = 0; i < current_solution.size() - 2; ++i) {
					solution += x_rotation_move_names[current_solution[i]];
					solution += " ";
				}
				if (auf_adf.contains(current_solution[current_solution.size() - 2]) && auf_adf.contains(current_solution[current_solution.size() - 1])) {
					solution += "(";
					solution += x_rotation_move_names[current_solution[current_solution.size() - 2]];
					solution += " ";
					solution += x_rotation_move_names[current_solution[current_solution.size() - 1]];
					solution += ")";
				}
				else if (auf_adf.contains(current_solution[current_solution.size() - 1])) {
					solution += x_rotation_move_names[current_solution[current_solution.size() - 2]];
					solution += " (";
					solution += x_rotation_move_names[current_solution[current_solution.size() - 1]];
					solution += ")";
				}
				else {
					solution += x_rotation_move_names[current_solution[current_solution.size() - 2]];
					solution += " ";
					solution += x_rotation_move_names[current_solution[current_solution.size() - 1]];
				}
			}
			++count;
			if (count > solutions) {
				exit(0);
			}
			std::cout << solution << std::endl;
			solution = "";

			return true;
		}

		if (depth == 0) {
			return false;
		}

		if ((((co_index * 40320 + cp_index) % 2 == 0) ? (co_cp_prune_table_E[(co_index * 40320 + cp_index) / 2] >> 4) : (co_cp_prune_table_E[(co_index * 40320 + cp_index) / 2] & 0b00001111)) > depth) {
			return false;
		}
		int prev_move;
		if (!(current_solution.empty())) {
			prev_move = current_solution.back();
		}
		else {
			prev_move = -1;
		}

		for (int move_num : move_name_index_E) {
			if (prev_move == -1) {
				if (move_num == forbidden || move_num == (forbidden + 1) || move_num == (forbidden + 2)) {
					continue;
				}
				else {
					goto PASS;
				}
			}
			if (!(is_move_available[prev_move][move_num])) {
				continue;
			}
		PASS:
			current_solution.push_back(move_num);
			next_co_index = co_move_table_E[co_index][move_num];
			next_eo_index = eo_move_table_E[eo_index][move_num];
			next_cp_index = cp_move_table_E[cp_index][move_num];
			next_mep_index = ep_move_table_E[mep_index][move_num];
			next_eep_index = ep_move_table_E[eep_index][move_num];
			next_sep_index = ep_move_table_E[sep_index][move_num];
			limited_search_COLL(next_co_index, next_eo_index, next_cp_index, next_mep_index, next_eep_index, next_sep_index, depth - 1);
			current_solution.pop_back();
		}
		return false;
	}

	void start_search(int min_length, int max_length, int sol_num) {
		max_solution_length = max_length;
		solutions = sol_num;
		int co_index = co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int cp_index = cp_to_index(initial_state.cp);
		int mep_index = MEP_to_index(initial_state.ep);
		int eep_index = EEP_to_index(initial_state.ep);
		int sep_index = SEP_to_index(initial_state.ep);
		int min_depth = min_length;

		while (min_depth <= max_solution_length) {
			std::cout << "\nstart searching in depth" << min_depth << "\n" << std::endl;
			if (limited_search_COLL(co_index, eo_index, cp_index, mep_index, eep_index, sep_index, min_depth)) {
				;
			}
			++min_depth;
		}
		return;
	}
};

struct Search_COLL1 {

	State initial_state;

	int max_solution_length;
	int solutions;
	int count = 0;

	std::vector<int> current_solution;
	int next_co_index;
	int next_eo_index;
	int next_cp_index;
	int next_mep_index;
	int next_eep_index;
	int next_sep_index;

	bool found;

	std::unordered_map<int, int> inv = { { 0, 3 }, { 12, 15 }, { 15, 12 } };
	std::set<int> auf_adf = { forbidden, forbidden + 2, inv[forbidden], inv[forbidden] + 2 };

	std::string solution;

	Search_COLL1(State arg_state) {
		initial_state = arg_state;
	}

	bool limited_search_COLL(int co_index, int eo_index, int cp_index, int mep_index, int eep_index, int sep_index, int depth) {
		found = false;
		if (co_index == 0 && eo_index == 0 && cp_index == 0 && meplist.contains(mep_index) && eep_index == 0 && seplist.contains(sep_index)) {
			if (depth != 0) {
				return false;
			}

			if (brackets) {
				for (int sol : current_solution) {
					solution += x_rotation_move_names[sol];
					solution += " ";
				}
			}
			else {
				for (int i = 0; i < current_solution.size() - 2; ++i) {
					solution += x_rotation_move_names[current_solution[i]];
					solution += " ";
				}
				if (auf_adf.contains(current_solution[current_solution.size() - 2]) && auf_adf.contains(current_solution[current_solution.size() - 1])) {
					solution += "(";
					solution += x_rotation_move_names[current_solution[current_solution.size() - 2]];
					solution += " ";
					solution += x_rotation_move_names[current_solution[current_solution.size() - 1]];
					solution += ")";
				}
				else if (auf_adf.contains(current_solution[current_solution.size() - 1])) {
					solution += x_rotation_move_names[current_solution[current_solution.size() - 2]];
					solution += " (";
					solution += x_rotation_move_names[current_solution[current_solution.size() - 1]];
					solution += ")";
				}
				else {
					solution += x_rotation_move_names[current_solution[current_solution.size() - 2]];
					solution += " ";
					solution += x_rotation_move_names[current_solution[current_solution.size() - 1]];
				}
			}
			++count;
			if (count > solutions) {
				exit(0);
			}
			std::cout << solution << std::endl;
			solution = "";

			return true;
		}

		if (depth == 0) {
			return false;
		}

		if (std::max({ (((co_index * 40320 + cp_index) % 2 == 0) ? (co_cp_prune_table_E[(co_index * 40320 + cp_index) / 2] >> 4) : (co_cp_prune_table_E[(co_index * 40320 + cp_index) / 2] & 0b00001111)),
						(((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
						(((cp_index * 11880 + eep_index) % 2 == 0) ? (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] >> 4) : (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] & 0b00001111)),
						(((eo_index * 40320 + cp_index) % 2 == 0) ? (eo_cp_prune_table_E[(eo_index * 40320 + cp_index) / 2] >> 4) : (eo_cp_prune_table_E[(eo_index * 40320 + cp_index) / 2] & 0b00001111)) }) > depth) {
			return false;
		}
		int prev_move;
		if (!(current_solution.empty())) {
			prev_move = current_solution.back();
		}
		else {
			prev_move = -1;
		}

		for (int move_num : move_name_index_E) {
			if (prev_move == -1) {
				if (move_num == forbidden || move_num == (forbidden + 2)) {
					continue;
				}
				else {
					goto PASS;
				}
			}
			if (!(is_move_available[prev_move][move_num])) {
				continue;
			}
		PASS:
			current_solution.push_back(move_num);
			next_co_index = co_move_table_E[co_index][move_num];
			next_eo_index = eo_move_table_E[eo_index][move_num];
			next_cp_index = cp_move_table_E[cp_index][move_num];
			next_mep_index = ep_move_table_E[mep_index][move_num];
			next_eep_index = ep_move_table_E[eep_index][move_num];
			next_sep_index = ep_move_table_E[sep_index][move_num];
			limited_search_COLL(next_co_index, next_eo_index, next_cp_index, next_mep_index, next_eep_index, next_sep_index, depth - 1);
			current_solution.pop_back();
		}
		return false;
	}

	void start_search(int min_length, int max_length, int sol_num) {
		max_solution_length = max_length;
		solutions = sol_num;
		int co_index = co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int cp_index = cp_to_index(initial_state.cp);
		int mep_index = MEP_to_index(initial_state.ep);
		int eep_index = EEP_to_index(initial_state.ep);
		int sep_index = SEP_to_index(initial_state.ep);
		int min_depth = min_length;

		while (min_depth <= max_solution_length) {
			std::cout << "\nstart searching in depth" << min_depth << "\n" << std::endl;
			if (limited_search_COLL(co_index, eo_index, cp_index, mep_index, eep_index, sep_index, min_depth)) {
				;
			}
			++min_depth;
		}
		return;
	}
};

struct Search_COLL2 {

	State_fs initial_state;

	int max_solution_length;
	int solutions;
	int count = 0;

	std::vector<int> current_solution;
	int next_co_index;
	int next_eo_index;
	int next_cp_index;
	int next_mep_index;
	int next_eep_index;
	int next_sep_index;
	int next_center_index;

	bool found;

	std::unordered_map<int, int> inv = { { 0, 3 }, { 12, 15 }, { 15, 12 } };
	std::set<int> auf_adf = { forbidden, forbidden + 1, forbidden + 2, inv[forbidden], inv[forbidden] + 1, inv[forbidden] + 2 };

	std::string solution;

	Search_COLL2(State_fs arg_state) {
		initial_state = arg_state;
	}

	bool limited_search_COLL_fs(int co_index, int eo_index, int cp_index, int mep_index, int eep_index, int sep_index, int center_index, int depth) {
		found = false;
		if (co_index == 0 && eo_index == 0 && cp_index == 0 && meplist.contains(mep_index) && eep_index == 0 && seplist.contains(sep_index) && center_index == 0) {
			if (depth != 0) {
				return false;
			}

			if (brackets) {
				for (int sol : current_solution) {
					solution += x_rotation_move_names[sol];
					solution += " ";
				}
			}
			else {
				for (int i = 0; i < current_solution.size() - 2; ++i) {
					solution += x_rotation_move_names[current_solution[i]];
					solution += " ";
				}
				if (auf_adf.contains(current_solution[current_solution.size() - 2]) && auf_adf.contains(current_solution[current_solution.size() - 1])) {
					solution += "(";
					solution += x_rotation_move_names[current_solution[current_solution.size() - 2]];
					solution += " ";
					solution += x_rotation_move_names[current_solution[current_solution.size() - 1]];
					solution += ")";
				}
				else if (auf_adf.contains(current_solution[current_solution.size() - 1])) {
					solution += x_rotation_move_names[current_solution[current_solution.size() - 2]];
					solution += " (";
					solution += x_rotation_move_names[current_solution[current_solution.size() - 1]];
					solution += ")";
				}
				else {
					solution += x_rotation_move_names[current_solution[current_solution.size() - 2]];
					solution += " ";
					solution += x_rotation_move_names[current_solution[current_solution.size() - 1]];
				}
			}
			++count;
			if (count > solutions) {
				exit(0);
			}
			std::cout << solution << std::endl;
			solution = "";

			return true;
		}

		if (depth == 0) {
			return false;
		}

		if (std::max({ (((co_index * 40320 + cp_index) % 2 == 0) ? (co_cp_prune_table_E[(co_index * 40320 + cp_index) / 2] >> 4) : (co_cp_prune_table_E[(co_index * 40320 + cp_index) / 2] & 0b00001111)),
						(((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
						(((co_index * 2048 * 24 + eo_index * 24 + center_index) % 2 == 0) ? (co_eo_center_prune_table_E[(co_index * 2048 * 24 + eo_index * 24 + center_index) / 2] >> 4) : (co_eo_center_prune_table_E[(co_index * 2048 * 24 + eo_index * 24 + center_index) / 2] & 0b00001111)) }) > depth) {
			return false;
		}
		int prev_move;
		if (!(current_solution.empty())) {
			prev_move = current_solution.back();
		}
		else {
			prev_move = -1;
		}

		for (int move_num : move_name_index_E) {
			if (prev_move == -1) {
				if (move_num == forbidden || move_num == (forbidden + 1) || move_num == (forbidden + 2) || move_num == (forbidden + 18) || move_num == (forbidden + 19) || move_num == (forbidden + 20)) {
					continue;
				}
				else {
					goto PASS;
				}
			}
			if (!(is_move_available[prev_move][move_num])) {
				continue;
			}
		PASS:
			current_solution.push_back(move_num);
			next_co_index = co_move_table_E[co_index][move_num];
			next_eo_index = eo_move_table_E[eo_index][move_num];
			next_cp_index = cp_move_table_E[cp_index][move_num];
			next_mep_index = ep_move_table_E[mep_index][move_num];
			next_eep_index = ep_move_table_E[eep_index][move_num];
			next_sep_index = ep_move_table_E[sep_index][move_num];
			next_center_index = center_move_table_E[center_index][move_num];
			limited_search_COLL_fs(next_co_index, next_eo_index, next_cp_index, next_mep_index, next_eep_index, next_sep_index, next_center_index, depth - 1);
			current_solution.pop_back();
		}
		return false;
	}

	void start_search_fs(int min_length, int max_length, int sol_num) {
		max_solution_length = max_length;
		solutions = sol_num;
		int co_index = co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int cp_index = cp_to_index(initial_state.cp);
		int mep_index = MEP_to_index(initial_state.ep);
		int eep_index = EEP_to_index(initial_state.ep);
		int sep_index = SEP_to_index(initial_state.ep);
		int center_index = center_to_index(initial_state.center);
		int min_depth = min_length;

		while (min_depth <= max_solution_length) {
			std::cout << "\nstart searching in depth" << min_depth << "\n" << std::endl;
			if (limited_search_COLL_fs(co_index, eo_index, cp_index, mep_index, eep_index, sep_index, center_index, min_depth)) {
				;
			}
			++min_depth;
		}
		return;
	}
};

struct Search_COLL3 {

	State_fs initial_state;

	int max_solution_length;
	int solutions;
	int count = 0;

	std::vector<int> current_solution;
	int next_co_index;
	int next_eo_index;
	int next_cp_index;
	int next_mep_index;
	int next_eep_index;
	int next_sep_index;
	int next_center_index;

	bool found;

	std::unordered_map<int, int> inv = { { 0, 3 }, { 12, 15 }, { 15, 12 } };
	std::set<int> auf_adf = { forbidden, forbidden + 2, inv[forbidden], inv[forbidden] + 2 };

	std::string solution;

	Search_COLL3(State_fs arg_state) {
		initial_state = arg_state;
	}

	bool limited_search_COLL_fs(int co_index, int eo_index, int cp_index, int mep_index, int eep_index, int sep_index, int center_index, int depth) {
		found = false;
		if (co_index == 0 && eo_index == 0 && cp_index == 0 && meplist.contains(mep_index) && eep_index == 0 && seplist.contains(sep_index) && center_index == 0) {
			if (depth != 0) {
				return false;
			}

			if (brackets) {
				for (int sol : current_solution) {
					solution += x_rotation_move_names[sol];
					solution += " ";
				}
			}
			else {
				for (int i = 0; i < current_solution.size() - 2; ++i) {
					solution += x_rotation_move_names[current_solution[i]];
					solution += " ";
				}
				if (auf_adf.contains(current_solution[current_solution.size() - 2]) && auf_adf.contains(current_solution[current_solution.size() - 1])) {
					solution += "(";
					solution += x_rotation_move_names[current_solution[current_solution.size() - 2]];
					solution += " ";
					solution += x_rotation_move_names[current_solution[current_solution.size() - 1]];
					solution += ")";
				}
				else if (auf_adf.contains(current_solution[current_solution.size() - 1])) {
					solution += x_rotation_move_names[current_solution[current_solution.size() - 2]];
					solution += " (";
					solution += x_rotation_move_names[current_solution[current_solution.size() - 1]];
					solution += ")";
				}
				else {
					solution += x_rotation_move_names[current_solution[current_solution.size() - 2]];
					solution += " ";
					solution += x_rotation_move_names[current_solution[current_solution.size() - 1]];
				}
			}
			++count;
			if (count > solutions) {
				exit(0);
			}
			std::cout << solution << std::endl;
			solution = "";

			return true;
		}

		if (depth == 0) {
			return false;
		}

		if (std::max({ (((co_index * 40320 + cp_index) % 2 == 0) ? (co_cp_prune_table_E[(co_index * 40320 + cp_index) / 2] >> 4) : (co_cp_prune_table_E[(co_index * 40320 + cp_index) / 2] & 0b00001111)),
						(((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
						(((cp_index * 11880 + eep_index) % 2 == 0) ? (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] >> 4) : (cp_eep_prune_table_E[(cp_index * 11880 + eep_index) / 2] & 0b00001111)),
						(((co_index * 2048 * 24 + eo_index * 24 + center_index) % 2 == 0) ? (co_eo_center_prune_table_E[(co_index * 2048 * 24 + eo_index * 24 + center_index) / 2] >> 4) : (co_eo_center_prune_table_E[(co_index * 2048 * 24 + eo_index * 24 + center_index) / 2] & 0b00001111)) }) > depth) {
			return false;
		}
		int prev_move;
		if (!(current_solution.empty())) {
			prev_move = current_solution.back();
		}
		else {
			prev_move = -1;
		}

		for (int move_num : move_name_index_E) {
			if (prev_move == -1) {
				if (move_num == forbidden || move_num == (forbidden + 2) || move_num == (forbidden + 18) || move_num == (forbidden + 20)) {
					continue;
				}
				else {
					goto PASS;
				}
			}
			if (!(is_move_available[prev_move][move_num])) {
				continue;
			}
		PASS:
			current_solution.push_back(move_num);
			next_co_index = co_move_table_E[co_index][move_num];
			next_eo_index = eo_move_table_E[eo_index][move_num];
			next_cp_index = cp_move_table_E[cp_index][move_num];
			next_mep_index = ep_move_table_E[mep_index][move_num];
			next_eep_index = ep_move_table_E[eep_index][move_num];
			next_sep_index = ep_move_table_E[sep_index][move_num];
			next_center_index = center_move_table_E[center_index][move_num];
			limited_search_COLL_fs(next_co_index, next_eo_index, next_cp_index, next_mep_index, next_eep_index, next_sep_index, next_center_index, depth - 1);
			current_solution.pop_back();
		}
		return false;
	}

	void start_search_fs(int min_length, int max_length, int sol_num) {
		max_solution_length = max_length;
		solutions = sol_num;
		int co_index = co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int cp_index = cp_to_index(initial_state.cp);
		int mep_index = MEP_to_index(initial_state.ep);
		int eep_index = EEP_to_index(initial_state.ep);
		int sep_index = SEP_to_index(initial_state.ep);
		int center_index = center_to_index(initial_state.center);
		int min_depth = min_length;

		while (min_depth <= max_solution_length) {
			std::cout << "\nstart searching in depth" << min_depth << "\n" << std::endl;
			if (limited_search_COLL_fs(co_index, eo_index, cp_index, mep_index, eep_index, sep_index, center_index, min_depth)) {
				;
			}
			++min_depth;
		}
		return;
	}
};

struct Search_ZBLS0 {

	State initial_state;

	int max_solution_length;
	int solutions;
	int count = 0;

	std::vector<int> current_solution;
	int next_co_index;
	int next_eo_index;
	int next_cp_index;
	int next_mep_index;
	int next_eep_index;
	int next_sep_index;

	bool found;

	std::string solution;

	std::vector<std::string> move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'",
										"R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" };

	Search_ZBLS0(State arg_state) {
		initial_state = arg_state;
	}

	bool limited_search_ZBLS(int co_index, int eo_index, int cp_index, int mep_index, int eep_index, int sep_index, int depth) {
		found = false;
		if (co_index == solved_co && eo_index == 0 && cp_index == solved_cp && solved_mep.contains(mep_index) && solved_eep.contains(eep_index) && solved_sep.contains(sep_index)) {
			if (depth != 0) {
				return false;
			}

			for (int sol : current_solution) {
				solution += move_names[sol];
				solution += " ";
			}

			++count;
			if (count > solutions) {
                exit(0);
			}
			std::cout << solution << std::endl;
			solution = "";

			return true;
		}

		if (depth == 0) {
			return false;
		}

		if (std::max({ (((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
						(((eo_index * 11880 + eep_index) % 2 == 0) ? (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] >> 4) : (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] & 0b00001111)),
						(((co_index * 2048 + eo_index) % 2 == 0) ? (co_eo_prune_table_E[(co_index * 2048 + eo_index) / 2] >> 4) : (co_eo_prune_table_E[(co_index * 2048 + eo_index) / 2] & 0b00001111)) }) > depth) {
			return false;
		}

		int prev_move;
		if (!(current_solution.empty())) {
			prev_move = current_solution.back();
		}
		else {
			prev_move = -1;
		}

		for (int move_num : move_name_index_E) {
			if (prev_move == -1) {
				if (move_num == 0 || move_num == 1 || move_num == 2) {
					continue;
				}
				else {
					goto PASS;
				}
			}
			if (!(is_move_available[prev_move][move_num])) {
				continue;
			}
		PASS:
			current_solution.push_back(move_num);
			next_co_index = co_move_table_E[co_index][move_num];
			next_eo_index = eo_move_table_E[eo_index][move_num];
			next_cp_index = cp_move_table_E[cp_index][move_num];
			next_mep_index = ep_move_table_E[mep_index][move_num];
			next_eep_index = ep_move_table_E[eep_index][move_num];
			next_sep_index = ep_move_table_E[sep_index][move_num];
			limited_search_ZBLS(next_co_index, next_eo_index, next_cp_index, next_mep_index, next_eep_index, next_sep_index, depth - 1);
			current_solution.pop_back();
		}
		return false;
	}

	void start_search(int min_length, int max_length, int sol_num) {
		max_solution_length = max_length;
		solutions = sol_num;
		int co_index = F2L_co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int cp_index = F2L_cp_to_index(initial_state.cp);
		int mep_index = MEP_to_index(initial_state.ep);
		int eep_index = EEP_to_index(initial_state.ep);
		int sep_index = SEP_to_index(initial_state.ep);
		int min_depth = min_length;
		while (min_depth <= max_solution_length) {
			std::cout << "\nstart searching in depth" << min_depth << "\n" << std::endl;
			if (limited_search_ZBLS(co_index, eo_index, cp_index, mep_index, eep_index, sep_index, min_depth)) {
				;
			}
			++min_depth;
		}
		return;
	}
};

struct Search_ZBLS1 {

	State initial_state;

	int max_solution_length;
	int solutions;
	int count = 0;

	std::vector<int> current_solution;
	int next_co_index;
	int next_eo_index;
	int next_cp_index;
	int next_mep_index;
	int next_eep_index;
	int next_sep_index;

	bool found;

	std::string solution;

	std::vector<std::string> move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'",
										"R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" };

	Search_ZBLS1(State arg_state) {
		initial_state = arg_state;
	}

	bool limited_search_ZBLS(int co_index, int eo_index, int cp_index, int mep_index, int eep_index, int sep_index, int depth) {
		found = false;
		if (co_index == solved_co && eo_index == 0 && cp_index == solved_cp && solved_mep.contains(mep_index) && solved_eep.contains(eep_index) && solved_sep.contains(sep_index)) {
			if (depth != 0) {
				return false;
			}

			for (int sol : current_solution) {
				solution += move_names[sol];
				solution += " ";
			}

			++count;
			if (count > solutions) {
				exit(0);
			}
			std::cout << solution << std::endl;
			solution = "";

			return true;
		}

		if (depth == 0) {
			return false;
		}

		if (std::max({ (((co_index * 11880 + eep_index) % 2 == 0) ? (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] >> 4) : (co_eep_prune_table_E[(co_index * 11880 + eep_index) / 2] & 0b00001111)),
						(((co_index * 2048 + eo_index) % 2 == 0) ? (co_eo_prune_table_E[(co_index * 2048 + eo_index) / 2] >> 4) : (co_eo_prune_table_E[(co_index * 2048 + eo_index) / 2] & 0b00001111)),
						(((eo_index * 11880 + eep_index) % 2 == 0) ? (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] >> 4) : (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] & 0b00001111)) }) > depth) {
			return false;
		}

		int prev_move;
		if (!(current_solution.empty())) {
			prev_move = current_solution.back();
		}
		else {
			prev_move = -1;
		}

		for (int move_num : move_name_index_E) {
			if (prev_move == -1) {
				if (move_num == 0 || move_num == 2) {
					continue;
				}
				else {
					goto PASS;
				}
			}
			if (!(is_move_available[prev_move][move_num])) {
				continue;
			}
		PASS:
			current_solution.push_back(move_num);
			next_co_index = co_move_table_E[co_index][move_num];
			next_eo_index = eo_move_table_E[eo_index][move_num];
			next_cp_index = cp_move_table_E[cp_index][move_num];
			next_mep_index = ep_move_table_E[mep_index][move_num];
			next_eep_index = ep_move_table_E[eep_index][move_num];
			next_sep_index = ep_move_table_E[sep_index][move_num];
			limited_search_ZBLS(next_co_index, next_eo_index, next_cp_index, next_mep_index, next_eep_index, next_sep_index, depth - 1);
			current_solution.pop_back();
		}
		return false;
	}

	void start_search(int min_length, int max_length, int sol_num) {
		max_solution_length = max_length;
		solutions = sol_num;
		int co_index = F2L_co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int cp_index = F2L_cp_to_index(initial_state.cp);
		int mep_index = MEP_to_index(initial_state.ep);
		int eep_index = EEP_to_index(initial_state.ep);
		int sep_index = SEP_to_index(initial_state.ep);
		int min_depth = min_length;

		while (min_depth <= max_solution_length) {
			std::cout << "\nstart searching in depth" << min_depth << "\n" << std::endl;
			if (limited_search_ZBLS(co_index, eo_index, cp_index, mep_index, eep_index, sep_index, min_depth)) {
				;
			}
			++min_depth;
		}
		return;
	}
};

struct Search_ZBLS2 {

	State_fs initial_state;

	int max_solution_length;
	int solutions;
	int count = 0;

	std::vector<int> current_solution;
	int next_co_index;
	int next_eo_index;
	int next_cp_index;
	int next_mep_index;
	int next_eep_index;
	int next_sep_index;
	int next_center_index;

	bool found;

	std::string solution;

	std::vector<std::string> move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'",
											"R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" ,
											"Uw", "Uw2", "Uw'", "Dw", "Dw2", "Dw'", "Lw", "Lw2", "Lw'",
											"Rw", "Rw2", "Rw'", "Fw", "Fw2", "Fw'", "Bw", "Bw2", "Bw'",
											"M", "M2", "M'", "E", "E2", "E'", "S", "S2", "S'" };

	Search_ZBLS2(State_fs arg_state) {
		initial_state = arg_state;
	}

	bool limited_search_ZBLS_fs(int co_index, int eo_index, int cp_index, int mep_index, int eep_index, int sep_index, int center_index, int depth) {
		found = false;
		if (co_index == solved_co && eo_index == 0 && cp_index == solved_cp && solved_mep.contains(mep_index) && solved_eep.contains(eep_index) && solved_sep.contains(sep_index) && center_index == 0) {
			if (depth != 0) {
				return false;
			}

			for (int sol : current_solution) {
				solution += move_names[sol];
				solution += " ";
			}

			++count;
			if (count > solutions) {
				exit(0);
			}
			std::cout << solution << std::endl;
			solution = "";

			return true;
		}

		if (depth == 0) {
			return false;
		}

		if (std::max({ (((eo_index * 11880 + eep_index) % 2 == 0) ? (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] >> 4) : (eo_eep_prune_table_E[(eo_index * 11880 + eep_index) / 2] & 0b00001111)),
						(((co_index * 2048 * 24 + eo_index * 24 + center_index) % 2 == 0) ? (co_eo_center_prune_table_E[(co_index * 2048 * 24 + eo_index * 24 + center_index) / 2] >> 4) : (co_eo_center_prune_table_E[(co_index * 2048 * 24 + eo_index * 24 + center_index) / 2] & 0b00001111)),
						(((cp_index * 11880 * 24 + eep_index * 24 + center_index) % 2 == 0) ? (cp_eep_center_prune_table_E[(cp_index * 11880 * 24 + eep_index * 24 + center_index) / 2] >> 4) : (cp_eep_center_prune_table_E[(cp_index * 11880 * 24 + eep_index * 24 + center_index) / 2] & 0b00001111)) }) > depth) {
			return false;
		}

		int prev_move;
		if (!(current_solution.empty())) {
			prev_move = current_solution.back();
		}
		else {
			prev_move = -1;
		}

		for (int move_num : move_name_index_E) {
			if (prev_move == -1) {
				if (move_num == 0 || move_num == 1 || move_num == 2 || move_num == 18 || move_num == 19 || move_num == 20) {
					continue;
				}
				else {
					goto PASS;
				}
			}
			if (!(is_move_available[prev_move][move_num])) {
				continue;
			}
		PASS:
			current_solution.push_back(move_num);
			next_co_index = co_move_table_E[co_index][move_num];
			next_eo_index = eo_move_table_E[eo_index][move_num];
			next_cp_index = cp_move_table_E[cp_index][move_num];
			next_mep_index = ep_move_table_E[mep_index][move_num];
			next_eep_index = ep_move_table_E[eep_index][move_num];
			next_sep_index = ep_move_table_E[sep_index][move_num];
			next_center_index = center_move_table_E[center_index][move_num];
			limited_search_ZBLS_fs(next_co_index, next_eo_index, next_cp_index, next_mep_index, next_eep_index, next_sep_index, next_center_index, depth - 1);
			current_solution.pop_back();
		}
		return false;
	}

	void start_search_fs(int min_length, int max_length, int sol_num) {
		max_solution_length = max_length;
		solutions = sol_num;
		int co_index = F2L_co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int cp_index = F2L_cp_to_index(initial_state.cp);
		int mep_index = MEP_to_index(initial_state.ep);
		int eep_index = EEP_to_index(initial_state.ep);
		int sep_index = SEP_to_index(initial_state.ep);
		int center_index = center_to_index(initial_state.center);
		int min_depth = min_length;

		while (min_depth <= max_solution_length) {
			std::cout << "\nstart searching in depth" << min_depth << "\n" << std::endl;
			if (limited_search_ZBLS_fs(co_index, eo_index, cp_index, mep_index, eep_index, sep_index, center_index, min_depth)) {
				;
			}
			++min_depth;
		}
		return;
	}
};

struct Search_ZBLS3 {

	State_fs initial_state;

	int max_solution_length;
	int solutions;
	int count = 0;

	std::vector<int> current_solution;
	int next_co_index;
	int next_eo_index;
	int next_cp_index;
	int next_mep_index;
	int next_eep_index;
	int next_sep_index;
	int next_center_index;

	bool found;

	std::string solution;

	std::vector<std::string> move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'",
											"R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" ,
											"Uw", "Uw2", "Uw'", "Dw", "Dw2", "Dw'", "Lw", "Lw2", "Lw'",
											"Rw", "Rw2", "Rw'", "Fw", "Fw2", "Fw'", "Bw", "Bw2", "Bw'",
											"M", "M2", "M'", "E", "E2", "E'", "S", "S2", "S'" };

	Search_ZBLS3(State_fs arg_state) {
		initial_state = arg_state;
	}

	bool limited_search_ZBLS_fs(int co_index, int eo_index, int cp_index, int mep_index, int eep_index, int sep_index, int center_index, int depth) {
		found = false;
		if (co_index == solved_co && eo_index == 0 && cp_index == solved_cp && solved_mep.contains(mep_index) && solved_eep.contains(eep_index) && solved_sep.contains(sep_index) && center_index == 0) {
			if (depth != 0) {
				return false;
			}

			for (int sol : current_solution) {
				solution += move_names[sol];
				solution += " ";
			}

			++count;
			if (count > solutions) {
				exit(0);
			}
			std::cout << solution << std::endl;
			solution = "";

			return true;
		}

		if (depth == 0) {
			return false;
		}

		if (std::max({ (((co_index * 2048 * 24 + eo_index * 24 + center_index) % 2 == 0) ? (co_eo_center_prune_table_E[(co_index * 2048 * 24 + eo_index * 24 + center_index) / 2] >> 4) : (co_eo_center_prune_table_E[(co_index * 2048 * 24 + eo_index * 24 + center_index) / 2] & 0b00001111)),
						(((cp_index * 11880 * 24 + eep_index * 24 + center_index) % 2 == 0) ? (cp_eep_center_prune_table_E[(cp_index * 11880 * 24 + eep_index * 24 + center_index) / 2] >> 4) : (cp_eep_center_prune_table_E[(cp_index * 11880 * 24 + eep_index * 24 + center_index) / 2] & 0b00001111)) }) > depth) {
			return false;
		}

		int prev_move;
		if (!(current_solution.empty())) {
			prev_move = current_solution.back();
		}
		else {
			prev_move = -1;
		}

		for (int move_num : move_name_index_E) {
			if (prev_move == -1) {
				if (move_num == 0 || move_num == 2 || move_num == 18 || move_num == 20) {
					continue;
				}
				else {
					goto PASS;
				}
			}
			if (!(is_move_available[prev_move][move_num])) {
				continue;
			}
		PASS:
			current_solution.push_back(move_num);
			next_co_index = co_move_table_E[co_index][move_num];
			next_eo_index = eo_move_table_E[eo_index][move_num];
			next_cp_index = cp_move_table_E[cp_index][move_num];
			next_mep_index = ep_move_table_E[mep_index][move_num];
			next_eep_index = ep_move_table_E[eep_index][move_num];
			next_sep_index = ep_move_table_E[sep_index][move_num];
			next_center_index = center_move_table_E[center_index][move_num];
			limited_search_ZBLS_fs(next_co_index, next_eo_index, next_cp_index, next_mep_index, next_eep_index, next_sep_index, next_center_index, depth - 1);
			current_solution.pop_back();
		}
		return false;
	}

	void start_search_fs(int min_length, int max_length, int sol_num) {
		max_solution_length = max_length;
		solutions = sol_num;
		int co_index = F2L_co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int cp_index = F2L_cp_to_index(initial_state.cp);
		int mep_index = MEP_to_index(initial_state.ep);
		int eep_index = EEP_to_index(initial_state.ep);
		int sep_index = SEP_to_index(initial_state.ep);
		int center_index = center_to_index(initial_state.center);
		int min_depth = min_length;

		while (min_depth <= max_solution_length) {
			std::cout << "\nstart searching in depth" << min_depth << "\n" << std::endl;
			if (limited_search_ZBLS_fs(co_index, eo_index, cp_index, mep_index, eep_index, sep_index, center_index, min_depth)) {
				;
			}
			++min_depth;
		}
		return;
	}
};

struct Search_UD {

	State initial_state;

	double searching_time;

	int max_solution_length;

	std::vector<int> current_solution_ph1;
	int next_co_index;
	int next_eo_index;
	int next_e_comb_index;
	bool found_lim_ph1;

	int cp_index;
	int udep_index;
	int eep_index;
	int depth_ph2;

	std::vector<int> current_solution_ph2;
	bool found_lim_ph2;
	std::string solution;
	int next_cp_index;
	int next_udep_index;
	int next_eep_index;

	std::vector<std::string> move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'", "R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" };
	std::vector<std::string> move_names_ph2 = { "U", "U2", "U'", "D", "D2", "D'", "L2", "R2", "F2", "B2" };

	Search_UD(State arg_state) {
		initial_state = arg_state;
	}

	bool depth_limited_search_ph1(int co_index, int eo_index, int e_comb_index, int depth_lim_ph1) {
		found_lim_ph1 = false;
		if (depth_lim_ph1 == 0 && co_index == 0 && eo_index == 0 && e_comb_index == 0) {
			int last_move_lim_ph1;
			if (current_solution_ph1.empty()) {
				last_move_lim_ph1 = -1;
			}
			else {
				last_move_lim_ph1 = current_solution_ph1.back();
			}

			if (last_move_lim_ph1 == -1 || last_move_lim_ph1 == 9 || last_move_lim_ph1 == 6 || last_move_lim_ph1 == 12 || last_move_lim_ph1 == 15 || last_move_lim_ph1 == 11 || last_move_lim_ph1 == 8 || last_move_lim_ph1 == 14 || last_move_lim_ph1 == 17) {
				State state_lim_ph1 = initial_state;
				for (int move_num : current_solution_ph1) {
					state_lim_ph1 = state_lim_ph1.apply_move(moves[move_num]);
				}
				return start_phase2(state_lim_ph1);
			}
		}
		if (depth_lim_ph1 == 0) {
			return false;
		}

		//枝刈り
		if (std::max(co_eec_prune_table[co_index][e_comb_index], eo_eec_prune_table[eo_index][e_comb_index]) > depth_lim_ph1) {
			return false;
		}

		int prev_move_lim_ph1;
		if (current_solution_ph1.empty()) {
			prev_move_lim_ph1 = -1;
		}
		else {
			prev_move_lim_ph1 = current_solution_ph1.back();
		}
		for (int move_num : move_name_index) {
			if (prev_move_lim_ph1 == -1) {
				goto PASS;
			}
			if (!(is_move_available[prev_move_lim_ph1][move_num])) {
				continue;
			}
		PASS:
			current_solution_ph1.push_back(move_num);
			next_co_index = co_move_table[co_index][move_num];
			next_eo_index = eo_move_table[eo_index][move_num];
			next_e_comb_index = e_combination_table[e_comb_index][move_num];
			found_lim_ph1 = depth_limited_search_ph1(next_co_index, next_eo_index, next_e_comb_index, depth_lim_ph1 - 1);
			current_solution_ph1.pop_back();
		}
		return found_lim_ph1;
	}

	bool depth_limited_search_ph2(int cp_index, int udep_index, int eep_index, int depth_lim_ph2) {

		if (depth_lim_ph2 == 0 && cp_index == 0 && udep_index == 0 && eep_index == 0) {
			if (last_solution_length.empty()) {
				for (int sol1 : current_solution_ph1) {
					solution += move_names[sol1];
					solution += " ";
				}
				solution += ".";
				for (int sol2 : current_solution_ph2) {
					solution += move_names_ph2[sol2];
					solution += " ";
				}
				std::cout << "Solution:" << solution << "\n(" << current_solution_ph1.size() + current_solution_ph2.size() << "moves)" << " in " << clock() - searching_time << " ms (UD)" << std::endl;
				max_solution_length = current_solution_ph1.size() + current_solution_ph2.size() - 1;
				solution = "";
				last_solution_length.push(current_solution_ph1.size() + current_solution_ph2.size());
				return true;
			}
			else {
				if (last_solution_length.top() > current_solution_ph1.size() + current_solution_ph2.size()) {
					for (int sol1 : current_solution_ph1) {
						solution += move_names[sol1];
						solution += " ";
					}
					solution += ".";
					for (int sol2 : current_solution_ph2) {
						solution += move_names_ph2[sol2];
						solution += " ";
					}
					std::cout << "Solution:" << solution << "\n(" << current_solution_ph1.size() + current_solution_ph2.size() << "moves)" << " in " << clock() - searching_time << " ms (UD) " << std::endl;
					max_solution_length = current_solution_ph1.size() + current_solution_ph2.size() - 1;
					solution = "";
					last_solution_length.pop();
					last_solution_length.push(current_solution_ph1.size() + current_solution_ph2.size());
					return true;
				}
			}
		}
		if (depth_lim_ph2 == 0) {
			return false;
		}

		//枝刈り
		if (std::max(cp_eep_prune_table[cp_index][eep_index], udep_eep_prune_table[udep_index][eep_index]) > depth_lim_ph2) {
			return false;
		}
		int prev_move_lim_ph2;
		if (!(current_solution_ph2.empty())) {
			prev_move_lim_ph2 = current_solution_ph2.back();
		}
		else if (!(current_solution_ph1.empty())) {
			prev_move_lim_ph2 = current_solution_ph1.back();
		}
		else {
			prev_move_lim_ph2 = -1;
		}

		for (int move_num : move_name_index_ph2) {
			if (prev_move_lim_ph2 == -1) {
				goto PASS2;
			}
			if (!(is_move_available[prev_move_lim_ph2][move_num])) {
				continue;
			}
		PASS2:

			if (move_num == 7) {
				move_num = 6;
			}
			if (move_num == 10) {
				move_num = 7;
			}
			if (move_num == 13) {
				move_num = 8;
			}
			if (move_num == 16) {
				move_num = 9;
			}
			current_solution_ph2.push_back(move_num);
			next_cp_index = cp_move_table[cp_index][move_num];
			next_udep_index = ud_ep_move_table[udep_index][move_num];
			next_eep_index = e_ep_move_table[eep_index][move_num];
			found_lim_ph2 = depth_limited_search_ph2(next_cp_index, next_udep_index, next_eep_index, depth_lim_ph2 - 1);
			current_solution_ph2.pop_back();
			if (found_lim_ph2) {
				return true;
			}
		}
		return false;
	}

	void start_search1(int min_length, int max_length) {
		max_solution_length = max_length;
		int co_index = co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int e_comb_index = e_combination_to_index(initial_state.ep);
		//std::cout << co_index << std::endl;
		//std::cout << eo_index << std::endl;
		//std::cout << e_comb_index << std::endl;
		int depth_ph1 = min_length;

		searching_time = clock();
		while (depth_ph1 <= max_solution_length) {
			//std::cout << "# Start searching phase 1 length " << depth_ph1 << " (UD)" << std::endl;
			if (depth_limited_search_ph1(co_index, eo_index, e_comb_index, depth_ph1)) {
				//std::cout << depth_ph1 << std::endl;
				//std::cout << "Found solution " << "current_solution_ph1.size() + current_solution_ph2.size()" << " length in start search1 (UD)" << std::endl;
				;
			}
			++depth_ph1;
		}
		return;
	}

	bool start_phase2(State state_ph2) {
		cp_index = cp_to_index(state_ph2.cp);
		udep_index = ud_ep_to_index(state_ph2.ep);
		eep_index = e_ep_to_index(state_ph2.ep);
		//std::cout << cp_index << std::endl;
		//std::cout << udep_index << std::endl;
		//std::cout << eep_index << std::endl;

		depth_ph2 = 0;

		while (depth_ph2 <= max_solution_length - current_solution_ph1.size()) {
			if (depth_limited_search_ph2(cp_index, udep_index, eep_index, depth_ph2)) {
				//std::cout << "Found solution " << current_solution_ph1.size() + current_solution_ph2.size() << " length in start phase 2" << std::endl;;
				return true;
			}
			++depth_ph2;
		}
		return false;
	}
};

struct Search_RL {

	State initial_state;

	double searching_time;

	int max_solution_length;

	std::vector<int> current_solution_ph1;
	int next_co_index;
	int next_eo_index;
	int next_e_comb_index;
	bool found_lim_ph1;

	int cp_index;
	int udep_index;
	int eep_index;
	int depth_ph2;

	std::vector<int> current_solution_ph2;
	bool found_lim_ph2;
	std::string solution;
	int next_cp_index;
	int next_udep_index;
	int next_eep_index;

	std::vector<std::string> move_names = { "R", "R2", "R'", "L", "L2", "L'", "U", "U2", "U'", "D", "D2", "D'", "F", "F2", "F'", "B", "B2", "B'" };
	std::vector<std::string> move_names_ph2 = { "R", "R2", "R'", "L", "L2", "L'", "U2", "D2", "F2", "B2" };

	Search_RL(State arg_state) {
		initial_state = arg_state;
	}

	bool depth_limited_search_ph1(int co_index, int eo_index, int e_comb_index, int depth_lim_ph1) {
		found_lim_ph1 = false;
		if (depth_lim_ph1 == 0 && co_index == 0 && eo_index == 0 && e_comb_index == 0) {
			int last_move_lim_ph1;
			if (current_solution_ph1.empty()) {
				last_move_lim_ph1 = -1;
			}
			else {
				last_move_lim_ph1 = current_solution_ph1.back();
			}

			if (last_move_lim_ph1 == -1 || last_move_lim_ph1 == 9 || last_move_lim_ph1 == 6 || last_move_lim_ph1 == 12 || last_move_lim_ph1 == 15 || last_move_lim_ph1 == 11 || last_move_lim_ph1 == 8 || last_move_lim_ph1 == 14 || last_move_lim_ph1 == 17) {
				State state_lim_ph1 = initial_state;
				for (int move_num : current_solution_ph1) {
					state_lim_ph1 = state_lim_ph1.apply_move(moves[move_num]);
				}
				return start_phase2(state_lim_ph1);
			}
		}
		if (depth_lim_ph1 == 0) {
			return false;
		}

		//枝刈り
		if (std::max(co_eec_prune_table[co_index][e_comb_index], eo_eec_prune_table[eo_index][e_comb_index]) > depth_lim_ph1) {
			return false;
		}

		int prev_move_lim_ph1;
		if (current_solution_ph1.empty()) {
			prev_move_lim_ph1 = -1;
		}
		else {
			prev_move_lim_ph1 = current_solution_ph1.back();
		}
		for (int move_num : move_name_index) {
			if (prev_move_lim_ph1 == -1) {
				goto PASS;
			}
			if (!(is_move_available[prev_move_lim_ph1][move_num])) {
				continue;
			}
		PASS:
			current_solution_ph1.push_back(move_num);
			next_co_index = co_move_table[co_index][move_num];
			next_eo_index = eo_move_table[eo_index][move_num];
			next_e_comb_index = e_combination_table[e_comb_index][move_num];
			found_lim_ph1 = depth_limited_search_ph1(next_co_index, next_eo_index, next_e_comb_index, depth_lim_ph1 - 1);
			current_solution_ph1.pop_back();
		}
		return found_lim_ph1;
	}

	bool depth_limited_search_ph2(int cp_index, int udep_index, int eep_index, int depth_lim_ph2) {

		if (depth_lim_ph2 == 0 && cp_index == 0 && udep_index == 0 && eep_index == 0) {
			if (last_solution_length.empty()) {
				for (int sol1 : current_solution_ph1) {
					solution += move_names[sol1];
					solution += " ";
				}
				solution += ".";
				for (int sol2 : current_solution_ph2) {
					solution += move_names_ph2[sol2];
					solution += " ";
				}
				std::cout << "Solution:" << solution << "\n(" << current_solution_ph1.size() + current_solution_ph2.size() << "moves)" << " in " << clock() - searching_time << " ms (RL)" << std::endl;
				max_solution_length = current_solution_ph1.size() + current_solution_ph2.size() - 1;
				solution = "";
				last_solution_length.push(current_solution_ph1.size() + current_solution_ph2.size());
				return true;
			}
			else {
				if (last_solution_length.top() > current_solution_ph1.size() + current_solution_ph2.size()) {
					for (int sol1 : current_solution_ph1) {
						solution += move_names[sol1];
						solution += " ";
					}
					solution += ".";
					for (int sol2 : current_solution_ph2) {
						solution += move_names_ph2[sol2];
						solution += " ";
					}
					std::cout << "Solution:" << solution << "\n(" << current_solution_ph1.size() + current_solution_ph2.size() << "moves)" << " in " << clock() - searching_time << " ms (RL)" << std::endl;
					max_solution_length = current_solution_ph1.size() + current_solution_ph2.size() - 1;
					solution = "";
					last_solution_length.pop();
					last_solution_length.push(current_solution_ph1.size() + current_solution_ph2.size());
					return true;
				}
			}
		}
		if (depth_lim_ph2 == 0) {
			return false;
		}

		//枝刈り
		if (std::max(cp_eep_prune_table[cp_index][eep_index], udep_eep_prune_table[udep_index][eep_index]) > depth_lim_ph2) {
			return false;
		}
		int prev_move_lim_ph2;
		if (!(current_solution_ph2.empty())) {
			prev_move_lim_ph2 = current_solution_ph2.back();
		}
		else if (!(current_solution_ph1.empty())) {
			prev_move_lim_ph2 = current_solution_ph1.back();
		}
		else {
			prev_move_lim_ph2 = -1;
		}

		for (int move_num : move_name_index_ph2) {
			if (prev_move_lim_ph2 == -1) {
				goto PASS2;
			}
			if (!(is_move_available[prev_move_lim_ph2][move_num])) {
				continue;
			}
		PASS2:

			if (move_num == 7) {
				move_num = 6;
			}
			if (move_num == 10) {
				move_num = 7;
			}
			if (move_num == 13) {
				move_num = 8;
			}
			if (move_num == 16) {
				move_num = 9;
			}
			current_solution_ph2.push_back(move_num);
			next_cp_index = cp_move_table[cp_index][move_num];
			next_udep_index = ud_ep_move_table[udep_index][move_num];
			next_eep_index = e_ep_move_table[eep_index][move_num];
			found_lim_ph2 = depth_limited_search_ph2(next_cp_index, next_udep_index, next_eep_index, depth_lim_ph2 - 1);
			current_solution_ph2.pop_back();
			if (found_lim_ph2) {
				return true;
			}
		}
		return false;
	}

	void start_search1(int min_length, int max_length) {
		max_solution_length = max_length;
		int co_index = co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int e_comb_index = e_combination_to_index(initial_state.ep);
		//std::cout << co_index << std::endl;
		//std::cout << eo_index << std::endl;
		//std::cout << e_comb_index << std::endl;
		int depth_ph1 = min_length;

		searching_time = clock();
		while (depth_ph1 <= max_solution_length) {
			//std::cout << "# Start searching phase 1 length " << depth_ph1 << " (RL)" << std::endl;
			if (depth_limited_search_ph1(co_index, eo_index, e_comb_index, depth_ph1)) {
				//std::cout << "Found solution " << current_solution_ph1.size() + current_solution_ph2.size() << " length in start search1 (RL)" << std::endl;
				;
			}
			++depth_ph1;
		}
		return;
	}

	bool start_phase2(State state_ph2) {
		cp_index = cp_to_index(state_ph2.cp);
		udep_index = ud_ep_to_index(state_ph2.ep);
		eep_index = e_ep_to_index(state_ph2.ep);
		//std::cout << cp_index << std::endl;
		//std::cout << udep_index << std::endl;
		//std::cout << eep_index << std::endl;

		depth_ph2 = 0;

		while (depth_ph2 <= max_solution_length - current_solution_ph1.size()) {
			if (depth_limited_search_ph2(cp_index, udep_index, eep_index, depth_ph2)) {
				//std::cout << "Found solution " << current_solution_ph1.size() + current_solution_ph2.size() << " length in start phase 2" << std::endl;;
				return true;
			}
			++depth_ph2;
		}
		return false;
	}
};

struct Search_FB {

	State initial_state;

	double searching_time;

	int max_solution_length;

	std::vector<int> current_solution_ph1;
	int next_co_index;
	int next_eo_index;
	int next_e_comb_index;
	bool found_lim_ph1;

	int cp_index;
	int udep_index;
	int eep_index;
	int depth_ph2;

	std::vector<int> current_solution_ph2;
	bool found_lim_ph2;
	std::string solution;
	int next_cp_index;
	int next_udep_index;
	int next_eep_index;

	std::vector<std::string> move_names = { "F", "F2", "F'", "B", "B2", "B'", "L", "L2", "L'", "R", "R2", "R'", "D", "D2", "D'", "U", "U2", "U'" };
	std::vector<std::string> move_names_ph2 = { "F", "F2", "F'", "B", "B2", "B'", "L2", "R2", "D2", "U2" };

	Search_FB(State arg_state) {
		initial_state = arg_state;
	}

	bool depth_limited_search_ph1(int co_index, int eo_index, int e_comb_index, int depth_lim_ph1) {
		found_lim_ph1 = false;
		if (depth_lim_ph1 == 0 && co_index == 0 && eo_index == 0 && e_comb_index == 0) {
			int last_move_lim_ph1;
			if (current_solution_ph1.empty()) {
				last_move_lim_ph1 = -1;
			}
			else {
				last_move_lim_ph1 = current_solution_ph1.back();
			}

			if (last_move_lim_ph1 == -1 || last_move_lim_ph1 == 9 || last_move_lim_ph1 == 6 || last_move_lim_ph1 == 12 || last_move_lim_ph1 == 15 || last_move_lim_ph1 == 11 || last_move_lim_ph1 == 8 || last_move_lim_ph1 == 14 || last_move_lim_ph1 == 17) {
				State state_lim_ph1 = initial_state;
				for (int move_num : current_solution_ph1) {
					state_lim_ph1 = state_lim_ph1.apply_move(moves[move_num]);
				}
				return start_phase2(state_lim_ph1);
			}
		}
		if (depth_lim_ph1 == 0) {
			return false;
		}

		//枝刈り
		if (std::max(co_eec_prune_table[co_index][e_comb_index], eo_eec_prune_table[eo_index][e_comb_index]) > depth_lim_ph1) {
			return false;
		}

		int prev_move_lim_ph1;
		if (current_solution_ph1.empty()) {
			prev_move_lim_ph1 = -1;
		}
		else {
			prev_move_lim_ph1 = current_solution_ph1.back();
		}
		for (int move_num : move_name_index) {
			if (prev_move_lim_ph1 == -1) {
				goto PASS;
			}
			if (!(is_move_available[prev_move_lim_ph1][move_num])) {
				continue;
			}
		PASS:
			current_solution_ph1.push_back(move_num);
			next_co_index = co_move_table[co_index][move_num];
			next_eo_index = eo_move_table[eo_index][move_num];
			next_e_comb_index = e_combination_table[e_comb_index][move_num];
			found_lim_ph1 = depth_limited_search_ph1(next_co_index, next_eo_index, next_e_comb_index, depth_lim_ph1 - 1);
			current_solution_ph1.pop_back();
		}
		return found_lim_ph1;
	}

	bool depth_limited_search_ph2(int cp_index, int udep_index, int eep_index, int depth_lim_ph2) {

		if (depth_lim_ph2 == 0 && cp_index == 0 && udep_index == 0 && eep_index == 0) {
			if (last_solution_length.empty()) {
				for (int sol1 : current_solution_ph1) {
					solution += move_names[sol1];
					solution += " ";
				}
				solution += ".";
				for (int sol2 : current_solution_ph2) {
					solution += move_names_ph2[sol2];
					solution += " ";
				}
				std::cout << "Solution:" << solution << "\n(" << current_solution_ph1.size() + current_solution_ph2.size() << "moves)" << " in " << clock() - searching_time << " ms (FB)" << std::endl;
				max_solution_length = current_solution_ph1.size() + current_solution_ph2.size() - 1;
				solution = "";
				last_solution_length.push(current_solution_ph1.size() + current_solution_ph2.size());
				return true;
			}
			else {
				if (last_solution_length.top() > current_solution_ph1.size() + current_solution_ph2.size()) {
					for (int sol1 : current_solution_ph1) {
						solution += move_names[sol1];
						solution += " ";
					}
					solution += ".";
					for (int sol2 : current_solution_ph2) {
						solution += move_names_ph2[sol2];
						solution += " ";
					}
					std::cout << "Solution:" << solution << "\n(" << current_solution_ph1.size() + current_solution_ph2.size() << "moves)" << " in " << clock() - searching_time << " ms (FB)" << std::endl;
					max_solution_length = current_solution_ph1.size() + current_solution_ph2.size() - 1;
					solution = "";
					last_solution_length.pop();
					last_solution_length.push(current_solution_ph1.size() + current_solution_ph2.size());
					return true;
				}
			}
		}
		if (depth_lim_ph2 == 0) {
			return false;
		}

		//枝刈り
		if (std::max(cp_eep_prune_table[cp_index][eep_index], udep_eep_prune_table[udep_index][eep_index]) > depth_lim_ph2) {
			return false;
		}
		int prev_move_lim_ph2;
		if (!(current_solution_ph2.empty())) {
			prev_move_lim_ph2 = current_solution_ph2.back();
		}
		else if (!(current_solution_ph1.empty())) {
			prev_move_lim_ph2 = current_solution_ph1.back();
		}
		else {
			prev_move_lim_ph2 = -1;
		}

		for (int move_num : move_name_index_ph2) {
			if (prev_move_lim_ph2 == -1) {
				goto PASS2;
			}
			if (!(is_move_available[prev_move_lim_ph2][move_num])) {
				continue;
			}
		PASS2:

			if (move_num == 7) {
				move_num = 6;
			}
			if (move_num == 10) {
				move_num = 7;
			}
			if (move_num == 13) {
				move_num = 8;
			}
			if (move_num == 16) {
				move_num = 9;
			}
			current_solution_ph2.push_back(move_num);
			next_cp_index = cp_move_table[cp_index][move_num];
			next_udep_index = ud_ep_move_table[udep_index][move_num];
			next_eep_index = e_ep_move_table[eep_index][move_num];
			found_lim_ph2 = depth_limited_search_ph2(next_cp_index, next_udep_index, next_eep_index, depth_lim_ph2 - 1);
			current_solution_ph2.pop_back();
			if (found_lim_ph2) {
				return true;
			}
		}
		return false;
	}

	void start_search1(int min_length, int max_length) {
		max_solution_length = max_length;
		int co_index = co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int e_comb_index = e_combination_to_index(initial_state.ep);
		//std::cout << co_index << std::endl;
		//std::cout << eo_index << std::endl;
		//std::cout << e_comb_index << std::endl;
		int depth_ph1 = min_length;

		searching_time = clock();
		while (depth_ph1 <= max_solution_length) {
			//std::cout << "# Start searching phase 1 length " << depth_ph1 << " (FB)" << std::endl;
			if (depth_limited_search_ph1(co_index, eo_index, e_comb_index, depth_ph1)) {
				//std::cout << "Found solution " << current_solution_ph1.size() + current_solution_ph2.size() << " length in start search1 (FB)" << std::endl;
				;
			}
			++depth_ph1;
		}
		return;
	}

	bool start_phase2(State state_ph2) {
		cp_index = cp_to_index(state_ph2.cp);
		udep_index = ud_ep_to_index(state_ph2.ep);
		eep_index = e_ep_to_index(state_ph2.ep);
		//std::cout << cp_index << std::endl;
		//std::cout << udep_index << std::endl;
		//std::cout << eep_index << std::endl;

		depth_ph2 = 0;

		while (depth_ph2 <= max_solution_length - current_solution_ph1.size()) {
			if (depth_limited_search_ph2(cp_index, udep_index, eep_index, depth_ph2)) {
				//std::cout << "Found solution " << current_solution_ph1.size() + current_solution_ph2.size() << " length in start phase 2" << std::endl;;
				return true;
			}
			++depth_ph2;
		}
		return false;
	}
};

struct Search_for_Beginners {

	State initial_state;

	int max_solution_length;

	std::vector<int> current_solution_ph1;
	int next_co_index;
	int next_eo_index;
	int next_e_comb_index;
	bool found_lim_ph1;

	int cp_index;
	int udep_index;
	int eep_index;
	int depth_ph2;

	std::vector<int> current_solution_ph2;
	bool found_lim_ph2;
	std::string solution;
	int next_cp_index;
	int next_udep_index;
	int next_eep_index;

	std::vector<std::string> move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'", "R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" };
	std::vector<std::string> move_names_ph2 = { "U", "U2", "U'", "D", "D2", "D'", "L2", "R2", "F2", "B2" };

	Search_for_Beginners(State arg_state) {
		initial_state = arg_state;
	}

	bool depth_limited_search_ph1(int co_index, int eo_index, int e_comb_index, int depth_lim_ph1) {
		found_lim_ph1 = false;
		if (depth_lim_ph1 == 0 && co_index == 0 && eo_index == 0 && e_comb_index == 0) {
			int last_move_lim_ph1;
			if (current_solution_ph1.empty()) {
				last_move_lim_ph1 = -1;
			}
			else {
				last_move_lim_ph1 = current_solution_ph1.back();
			}

			if (last_move_lim_ph1 == -1 || last_move_lim_ph1 == 9 || last_move_lim_ph1 == 6 || last_move_lim_ph1 == 12 || last_move_lim_ph1 == 15 || last_move_lim_ph1 == 11 || last_move_lim_ph1 == 8 || last_move_lim_ph1 == 14 || last_move_lim_ph1 == 17) {
				State state_lim_ph1 = initial_state;
				for (int move_num : current_solution_ph1) {
					state_lim_ph1 = state_lim_ph1.apply_move(moves[move_num]);
				}
				return start_phase2(state_lim_ph1);
			}
		}
		if (depth_lim_ph1 == 0) {
			return false;
		}

		//枝刈り
		if (std::max(co_eec_prune_table[co_index][e_comb_index], eo_eec_prune_table[eo_index][e_comb_index]) > depth_lim_ph1) {
			return false;
		}

		int prev_move_lim_ph1;
		if (current_solution_ph1.empty()) {
			prev_move_lim_ph1 = -1;
		}
		else {
			prev_move_lim_ph1 = current_solution_ph1.back();
		}
		for (int move_num : move_name_index) {
			if (prev_move_lim_ph1 == -1) {
				goto PASS;
			}
			if (!(is_move_available[prev_move_lim_ph1][move_num])) {
				continue;
			}
		PASS:
			current_solution_ph1.push_back(move_num);
			next_co_index = co_move_table[co_index][move_num];
			next_eo_index = eo_move_table[eo_index][move_num];
			next_e_comb_index = e_combination_table[e_comb_index][move_num];
			found_lim_ph1 = depth_limited_search_ph1(next_co_index, next_eo_index, next_e_comb_index, depth_lim_ph1 - 1);
			current_solution_ph1.pop_back();
		}
		return found_lim_ph1;
	}

	bool depth_limited_search_ph2(int cp_index, int udep_index, int eep_index, int depth_lim_ph2) {

		if (depth_lim_ph2 == 0 && cp_index == 0 && udep_index == 0 && eep_index == 0) {
			if (last_solution_length.empty()) {
				for (int sol1 : current_solution_ph1) {
					solution += move_names[sol1];
					solution += " ";
				}
				for (int sol2 : current_solution_ph2) {
					solution += move_names_ph2[sol2];
					solution += " ";
				}
				std::cout << solution << std::endl;
				exit(0);
			}
		}
		if (depth_lim_ph2 == 0) {
			return false;
		}

		//枝刈り
		if (std::max(cp_eep_prune_table[cp_index][eep_index], udep_eep_prune_table[udep_index][eep_index]) > depth_lim_ph2) {
			return false;
		}
		int prev_move_lim_ph2;
		if (!(current_solution_ph2.empty())) {
			prev_move_lim_ph2 = current_solution_ph2.back();
		}
		else if (!(current_solution_ph1.empty())) {
			prev_move_lim_ph2 = current_solution_ph1.back();
		}
		else {
			prev_move_lim_ph2 = -1;
		}

		for (int move_num : move_name_index_ph2) {
			if (prev_move_lim_ph2 == -1) {
				goto PASS2;
			}
			if (!(is_move_available[prev_move_lim_ph2][move_num])) {
				continue;
			}
		PASS2:

			if (move_num == 7) {
				move_num = 6;
			}
			if (move_num == 10) {
				move_num = 7;
			}
			if (move_num == 13) {
				move_num = 8;
			}
			if (move_num == 16) {
				move_num = 9;
			}
			current_solution_ph2.push_back(move_num);
			next_cp_index = cp_move_table[cp_index][move_num];
			next_udep_index = ud_ep_move_table[udep_index][move_num];
			next_eep_index = e_ep_move_table[eep_index][move_num];
			found_lim_ph2 = depth_limited_search_ph2(next_cp_index, next_udep_index, next_eep_index, depth_lim_ph2 - 1);
			current_solution_ph2.pop_back();
			if (found_lim_ph2) {
				return true;
			}
		}
		return false;
	}

	void start_search1(int min_length, int max_length) {
		max_solution_length = max_length;
		int co_index = co_to_index(initial_state.co);
		int eo_index = eo_to_index(initial_state.eo);
		int e_comb_index = e_combination_to_index(initial_state.ep);
		//std::cout << co_index << std::endl;
		//std::cout << eo_index << std::endl;
		//std::cout << e_comb_index << std::endl;
		int depth_ph1 = min_length;

		while (depth_ph1 <= max_solution_length) {
			if (depth_limited_search_ph1(co_index, eo_index, e_comb_index, depth_ph1)) {
				;
			}
			++depth_ph1;
		}
		return;
	}

	bool start_phase2(State state_ph2) {
		cp_index = cp_to_index(state_ph2.cp);
		udep_index = ud_ep_to_index(state_ph2.ep);
		eep_index = e_ep_to_index(state_ph2.ep);
		//std::cout << cp_index << std::endl;
		//std::cout << udep_index << std::endl;
		//std::cout << eep_index << std::endl;

		depth_ph2 = 0;

		while (depth_ph2 <= max_solution_length - current_solution_ph1.size()) {
			if (depth_limited_search_ph2(cp_index, udep_index, eep_index, depth_ph2)) {
				return true;
			}
			++depth_ph2;
		}
		return false;
	}
};

int main(int argc, char* argv[]) {

/*
argc == 44 -> Search UD, Search RL, Search FB, Search for Beginners
argc == 67 -> F2L Explorer / pattern == 0 ~ 3 -> 0 slot solved, pattern == 4 ~ 9 -> 1 slot solved, pattern == 10 ~ 13 -> 2 slots solved, pattern == 14 -> 3 slots solved
argc == 69 -> PLL Explorer, OLL Explorer
argc == 70 -> sub step Explorer / pattern == 0 -> OLL+PLL, pattern == 1 -> OLL+CPLL, pattern == 2 -> LS+EOLL, pattern == 3 -> LS+OLL, pattern == 4,5 -> Advanced F2L
*/

	std::unordered_map<int, int> inv_face = {
		{0, 1},
		{1, 0},
		{2, 3},
		{3, 2},
		{4, 5},
		{5, 4},
	};

	if (argc == 44) {
		std::ifstream ifs("pre_culculation.json");
		IStreamWrapper isw(ifs);
		Document doc;
		doc.ParseStream(isw);

		co_move_table.reserve(2187);

		const Value& co_move_tbl = doc["CO_MOVE_TABLE"].GetArray();
		for (auto& d : co_move_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(18);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			co_move_table.emplace_back(X);
		}

		eo_move_table.reserve(2048);

		const Value& eo_move_tbl = doc["EO_MOVE_TABLE"].GetArray();
		for (auto& d : eo_move_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(18);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			eo_move_table.emplace_back(X);
		}

		e_combination_table.reserve(495);

		const Value& e_combination_tbl = doc["E_COMBINATION_TABLE"].GetArray();
		for (auto& d : e_combination_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(18);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			e_combination_table.emplace_back(X);
		}

		cp_move_table.reserve(40320);

		const Value& cp_move_tbl = doc["CP_MOVE_TABLE"].GetArray();
		for (auto& d : cp_move_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(10);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			cp_move_table.emplace_back(X);
		}

		ud_ep_move_table.reserve(40320);

		const Value& ud_ep_move_tbl = doc["UD_EP_MOVE_TABLE"].GetArray();
		for (auto& d : ud_ep_move_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(10);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			ud_ep_move_table.emplace_back(X);
		}

		e_ep_move_table.reserve(24);

		const Value& e_ep_move_tbl = doc["E_EP_MOVE_TABLE"].GetArray();
		for (auto& d : e_ep_move_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(10);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			e_ep_move_table.emplace_back(X);
		}

		co_eec_prune_table.reserve(2187);

		const Value& co_eec_prune_tbl = doc["CO_EEC_PRUNE_TABLE"].GetArray();
		for (auto& d : co_eec_prune_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(495);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			co_eec_prune_table.emplace_back(X);
		}

		eo_eec_prune_table.reserve(2048);

		const Value& eo_eec_prune_tbl = doc["EO_EEC_PRUNE_TABLE"].GetArray();
		for (auto& d : eo_eec_prune_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(495);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			eo_eec_prune_table.emplace_back(X);
		}

		cp_eep_prune_table.reserve(40320);

		const Value& cp_eep_prune_tbl = doc["CP_EEP_PRUNE_TABLE"].GetArray();
		for (auto& d : cp_eep_prune_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(24);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			cp_eep_prune_table.emplace_back(X);
		}

		udep_eep_prune_table.reserve(40320);

		const Value& udep_eep_prune_tbl = doc["UDEP_EEP_PRUNE_TABLE"].GetArray();
		for (auto& d : udep_eep_prune_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(24);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			udep_eep_prune_table.emplace_back(X);
		}

		if (std::stoi(argv[43]) == 1) {
			std::vector<int> Cpp_cp;
			std::vector<int> Cpp_co;
			std::vector<int> Cpp_ep;
			std::vector<int> Cpp_eo;
			Cpp_cp.reserve(8);
			Cpp_co.reserve(8);
			Cpp_ep.reserve(12);
			Cpp_eo.reserve(12);

			for (int i = 1; i < 9; ++i) {
				Cpp_cp.emplace_back(std::stoi(argv[i]));
			}

			for (int i = 9; i < 17; ++i) {
				Cpp_co.emplace_back(std::stoi(argv[i]));
			}

			for (int i = 17; i < 29; ++i) {
				Cpp_ep.emplace_back(std::stoi(argv[i]));
			}

			for (int i = 29; i < 41; ++i) {
				Cpp_eo.emplace_back(std::stoi(argv[i]));
			}

			int min_length = std::stoi(argv[41]);
			int max_length = std::stoi(argv[42]);

			State scrambled_state(Cpp_cp, Cpp_co, Cpp_ep, Cpp_eo);

			Search_UD solution(scrambled_state);

			solution.start_search1(min_length, max_length);
		}

		else if (std::stoi(argv[43]) == 2) {
			std::vector<int> Cpp_cp;
			std::vector<int> Cpp_co;
			std::vector<int> Cpp_ep;
			std::vector<int> Cpp_eo;
			Cpp_cp.reserve(8);
			Cpp_co.reserve(8);
			Cpp_ep.reserve(12);
			Cpp_eo.reserve(12);

			for (int i = 1; i < 9; ++i) {
				Cpp_cp.emplace_back(std::stoi(argv[i]));
			}

			for (int i = 9; i < 17; ++i) {
				Cpp_co.emplace_back(std::stoi(argv[i]));
			}

			for (int i = 17; i < 29; ++i) {
				Cpp_ep.emplace_back(std::stoi(argv[i]));
			}

			for (int i = 29; i < 41; ++i) {
				Cpp_eo.emplace_back(std::stoi(argv[i]));
			}

			int min_length = std::stoi(argv[41]);
			int max_length = std::stoi(argv[42]);

			State scrambled_state(Cpp_cp, Cpp_co, Cpp_ep, Cpp_eo);

			Search_RL solution(scrambled_state);

			solution.start_search1(min_length, max_length);
		}

		else if (std::stoi(argv[43]) == 3) {
			std::vector<int> Cpp_cp;
			std::vector<int> Cpp_co;
			std::vector<int> Cpp_ep;
			std::vector<int> Cpp_eo;
			Cpp_cp.reserve(8);
			Cpp_co.reserve(8);
			Cpp_ep.reserve(12);
			Cpp_eo.reserve(12);

			for (int i = 1; i < 9; ++i) {
				Cpp_cp.emplace_back(std::stoi(argv[i]));
			}

			for (int i = 9; i < 17; ++i) {
				Cpp_co.emplace_back(std::stoi(argv[i]));
			}

			for (int i = 17; i < 29; ++i) {
				Cpp_ep.emplace_back(std::stoi(argv[i]));
			}

			for (int i = 29; i < 41; ++i) {
				Cpp_eo.emplace_back(std::stoi(argv[i]));
			}

			int min_length = std::stoi(argv[41]);
			int max_length = std::stoi(argv[42]);

			State scrambled_state(Cpp_cp, Cpp_co, Cpp_ep, Cpp_eo);

			Search_FB solution(scrambled_state);

			solution.start_search1(min_length, max_length);
		}

		else if (std::stoi(argv[43]) == 4) {
			std::vector<int> Cpp_cp;
			std::vector<int> Cpp_co;
			std::vector<int> Cpp_ep;
			std::vector<int> Cpp_eo;
			Cpp_cp.reserve(8);
			Cpp_co.reserve(8);
			Cpp_ep.reserve(12);
			Cpp_eo.reserve(12);

			for (int i = 1; i < 9; ++i) {
				Cpp_cp.emplace_back(std::stoi(argv[i]));
			}

			for (int i = 9; i < 17; ++i) {
				Cpp_co.emplace_back(std::stoi(argv[i]));
			}

			for (int i = 17; i < 29; ++i) {
				Cpp_ep.emplace_back(std::stoi(argv[i]));
			}

			for (int i = 29; i < 41; ++i) {
				Cpp_eo.emplace_back(std::stoi(argv[i]));
			}

			int min_length = std::stoi(argv[41]);
			int max_length = std::stoi(argv[42]);

			State scrambled_state(Cpp_cp, Cpp_co, Cpp_ep, Cpp_eo);

			Search_for_Beginners solution(scrambled_state);

			solution.start_search1(min_length, max_length);
		}
	}

	else if (argc == 67) {

		pattern = std::stoi(argv[66]);
		solved_co = solved_index1["co"][pattern];
		solved_cp = solved_index1["cp"][pattern];
		solved_eo = solved_index2["eo"][pattern];
		solved_mep = solved_index2["mep"][pattern];
		solved_eep = solved_index2["eep"][pattern];
		solved_sep = solved_index2["sep"][pattern];

		std::ifstream ifs1("pre_culculation_E.json");
		IStreamWrapper isw1(ifs1);
		Document doc1;
		doc1.ParseStream(isw1);

		eo_move_table_E.reserve(2048);

		const Value& eo_move_tbl = doc1["EO_MOVE_TABLE"].GetArray();
		for (auto& d : eo_move_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(45);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			eo_move_table_E.emplace_back(X);
		}

		ep_move_table_E.reserve(11880);

		const Value& ep_move_tbl = doc1["EP_MOVE_TABLE"].GetArray();
		for (auto& d : ep_move_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(45);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			ep_move_table_E.emplace_back(X);
		}

		if (pattern < 4) {

			std::ifstream ifs2("pre_culculation_F2L.json");
			IStreamWrapper isw2(ifs2);
			Document doc2;
			doc2.ParseStream(isw2);

			co_move_table_E.reserve(24);

			const Value& co_move_tbl = doc2["F2L_CO0_MOVE_TABLE"].GetArray();
			for (auto& d : co_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				co_move_table_E.emplace_back(X);
			}

			cp_move_table_E.reserve(8);

			const Value& cp_move_tbl = doc2["F2L_CP0_MOVE_TABLE"].GetArray();
			for (auto& d : cp_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				cp_move_table_E.emplace_back(X);
			}
		}

		else if (4 <= pattern && pattern < 10) {

			std::ifstream ifs2("pre_culculation_F2L.json");
			IStreamWrapper isw2(ifs2);
			Document doc2;
			doc2.ParseStream(isw2);

			co_move_table_E.reserve(252);

			const Value& co_move_tbl = doc2["F2L_CO1_MOVE_TABLE"].GetArray();
			for (auto& d : co_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				co_move_table_E.emplace_back(X);
			}

			cp_move_table_E.reserve(56);

			const Value& cp_move_tbl = doc2["F2L_CP1_MOVE_TABLE"].GetArray();
			for (auto& d : cp_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				cp_move_table_E.emplace_back(X);
			}
		}

		else if (10 <= pattern && pattern < 14) {

			std::ifstream ifs2("pre_culculation_F2L.json");
			IStreamWrapper isw2(ifs2);
			Document doc2;
			doc2.ParseStream(isw2);

			co_move_table_E.reserve(1512);

			const Value& co_move_tbl = doc2["F2L_CO2_MOVE_TABLE"].GetArray();
			for (auto& d : co_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				co_move_table_E.emplace_back(X);
			}

			cp_move_table_E.reserve(336);

			const Value& cp_move_tbl = doc2["F2L_CP2_MOVE_TABLE"].GetArray();
			for (auto& d : cp_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				cp_move_table_E.emplace_back(X);
			}
		}

		else if (pattern == 14) {
			
			std::ifstream ifs2("pre_culculation_F2L.json");
			IStreamWrapper isw2(ifs2);
			Document doc2;
			doc2.ParseStream(isw2);

			co_move_table_E.reserve(5670);

			const Value& co_move_tbl = doc2["F2L_CO3_MOVE_TABLE"].GetArray();
			for (auto& d : co_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				co_move_table_E.emplace_back(X);
			}

			cp_move_table_E.reserve(1680);

			const Value& cp_move_tbl = doc2["F2L_CP3_MOVE_TABLE"].GetArray();
			for (auto& d : cp_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				cp_move_table_E.emplace_back(X);
			}
		}

		if (std::stoi(argv[65]) == 0 || std::stoi(argv[65]) == 1) {

			std::vector<int> Cpp_cp;
			std::vector<int> Cpp_co;
			std::vector<int> Cpp_ep;
			std::vector<int> Cpp_eo;
			Cpp_cp.reserve(8);
			Cpp_co.reserve(8);
			Cpp_ep.reserve(12);
			Cpp_eo.reserve(12);

			for (int i = 1; i < 9; ++i) {
				Cpp_cp.emplace_back(std::stoi(argv[i]));
			}

			for (int i = 9; i < 17; ++i) {
				Cpp_co.emplace_back(std::stoi(argv[i]));
			}

			for (int i = 17; i < 29; ++i) {
				Cpp_ep.emplace_back(std::stoi(argv[i]));
			}

			for (int i = 29; i < 41; ++i) {
				Cpp_eo.emplace_back(std::stoi(argv[i]));
			}

			int min_length = std::stoi(argv[62]);
			int max_length = std::stoi(argv[63]);
			int sol_num = std::stoi(argv[64]);

			State scrambled_state(Cpp_cp, Cpp_co, Cpp_ep, Cpp_eo);

			if (std::stoi(argv[65]) == 0) {

				if (pattern < 4) {

					eo_mep_prune_table_E = new unsigned char[12165120];
					eo_sep_prune_table_E = new unsigned char[12165120];
					mep_sep_prune_table_E = new unsigned char[70567200];

					FILE* file0;
					fopen_s(&file0, (std::string("Tables\\eo_mep-0-0-") + std::to_string(pattern) + std::string(".bin")).c_str(), "rb");
					fread(eo_mep_prune_table_E, 1, 12165120, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, (std::string("Tables\\eo_sep-0-0-") + std::to_string(pattern) + std::string(".bin")).c_str(), "rb");
					fread(eo_sep_prune_table_E, 1, 12165120, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, (std::string("Tables\\mep_sep-0-0-") + std::to_string(pattern) + std::string(".bin")).c_str(), "rb");
					fread(mep_sep_prune_table_E, 1, 70567200, file2);
					fclose(file2);

					pattern = 0;
				}

				else if (4 <= pattern && pattern < 10) {

					co_eep_prune_table_E = new unsigned char[1496880];
					co_sep_prune_table_E = new unsigned char[1496880];
					co_mep_prune_table_E = new unsigned char[1496880];
					eo_eep_prune_table_E = new unsigned char[12165120];

					FILE* file0;
					fopen_s(&file0, (std::string("Tables\\co_eep-0-1-") + std::to_string(pattern - 4) + std::string(".bin")).c_str(), "rb");
					fread(co_eep_prune_table_E, 1, 1496880, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, (std::string("Tables\\co_sep-0-1-") + std::to_string(pattern - 4) + std::string(".bin")).c_str(), "rb");
					fread(co_sep_prune_table_E, 1, 1496880, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, (std::string("Tables\\co_mep-0-1-") + std::to_string(pattern - 4) + std::string(".bin")).c_str(), "rb");
					fread(co_mep_prune_table_E, 1, 1496880, file2);
					fclose(file2);

					FILE* file3;
					fopen_s(&file3, (std::string("Tables\\eo_eep-0-1-") + std::to_string(pattern - 4) + std::string(".bin")).c_str(), "rb");
					fread(eo_eep_prune_table_E, 1, 12165120, file3);
					fclose(file3);

					pattern = 1;
				}

				else if (10 <= pattern && pattern < 14) {

					co_eep_prune_table_E = new unsigned char[8981280];
					co_sep_prune_table_E = new unsigned char[8981280];
					co_mep_prune_table_E = new unsigned char[8981280];
					eo_eep_prune_table_E = new unsigned char[12165120];

					FILE* file0;
					fopen_s(&file0, (std::string("Tables\\co_eep-0-2-") + std::to_string(pattern - 10) + std::string(".bin")).c_str(), "rb");
					fread(co_eep_prune_table_E, 1, 8981280, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, (std::string("Tables\\co_sep-0-2-") + std::to_string(pattern - 10) + std::string(".bin")).c_str(), "rb");
					fread(co_sep_prune_table_E, 1, 8981280, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, (std::string("Tables\\co_mep-0-2-") + std::to_string(pattern - 10) + std::string(".bin")).c_str(), "rb");
					fread(co_mep_prune_table_E, 1, 8981280, file2);
					fclose(file2);

					FILE* file3;
					fopen_s(&file3, (std::string("Tables\\eo_eep-0-2-") + std::to_string(pattern - 10) + std::string(".bin")).c_str(), "rb");
					fread(eo_eep_prune_table_E, 1, 12165120, file3);
					fclose(file3);

					pattern = 2;
				}

				else if (pattern == 14) {
					
					co_eep_prune_table_E = new unsigned char[33679800];
					co_sep_prune_table_E = new unsigned char[33679800];
					co_mep_prune_table_E = new unsigned char[33679800];
					eo_eep_prune_table_E = new unsigned char[12165120];
					cp_eep_prune_table_E = new unsigned char[9979200];

					FILE* file0;
					fopen_s(&file0, (std::string("Tables\\co_eep-0-3-") + std::to_string(pattern - 14) + std::string(".bin")).c_str(), "rb");
					fread(co_eep_prune_table_E, 1, 33679800, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, (std::string("Tables\\co_sep-0-3-") + std::to_string(pattern - 14) + std::string(".bin")).c_str(), "rb");
					fread(co_sep_prune_table_E, 1, 33679800, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, (std::string("Tables\\co_mep-0-3-") + std::to_string(pattern - 14) + std::string(".bin")).c_str(), "rb");
					fread(co_mep_prune_table_E, 1, 33679800, file2);
					fclose(file2);

					FILE* file3;
					fopen_s(&file3, (std::string("Tables\\eo_eep-0-3-") + std::to_string(pattern - 14) + std::string(".bin")).c_str(), "rb");
					fread(eo_eep_prune_table_E, 1, 12165120, file3);
					fclose(file3);

					FILE* file4;
					fopen_s(&file4, (std::string("Tables\\cp_eep-0-3-") + std::to_string(pattern - 14) + std::string(".bin")).c_str(), "rb");
					fread(cp_eep_prune_table_E, 1, 9979200, file4);
					fclose(file4);

					pattern = 3;
				}

				for (int i = 47; i < 53; ++i) {
					if (std::stoi(argv[i]) == 1) {
						move_name_index_E.emplace_back(3 * i - 141);
						move_name_index_E.emplace_back(3 * i - 140);
						move_name_index_E.emplace_back(3 * i - 139);
					}
				}
				
				Search_F2L0 solution(scrambled_state);

				solution.start_search(min_length, max_length, sol_num);
			}

			else if (std::stoi(argv[65]) == 1) {

				if (pattern < 4) {

					eo_mep_prune_table_E = new unsigned char[12165120];
					eo_sep_prune_table_E = new unsigned char[12165120];

					FILE* file0;
					fopen_s(&file0, (std::string("Tables\\eo_mep-1-0-") + std::to_string(pattern) + std::string(".bin")).c_str(), "rb");
					fread(eo_mep_prune_table_E, 1, 12165120, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, (std::string("Tables\\eo_sep-1-0-") + std::to_string(pattern) + std::string(".bin")).c_str(), "rb");
					fread(eo_sep_prune_table_E, 1, 12165120, file1);
					fclose(file1);

					pattern = 0;
				}

				else if (4 <= pattern && pattern < 10) {

					co_eep_prune_table_E = new unsigned char[1496880];
					co_sep_prune_table_E = new unsigned char[1496880];
					co_mep_prune_table_E = new unsigned char[1496880];

					FILE* file0;
					fopen_s(&file0, (std::string("Tables\\co_eep-1-1-") + std::to_string(pattern - 4) + std::string(".bin")).c_str(), "rb");
					fread(co_eep_prune_table_E, 1, 1496880, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, (std::string("Tables\\co_sep-1-1-") + std::to_string(pattern - 4) + std::string(".bin")).c_str(), "rb");
					fread(co_sep_prune_table_E, 1, 1496880, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, (std::string("Tables\\co_mep-1-1-") + std::to_string(pattern - 4) + std::string(".bin")).c_str(), "rb");
					fread(co_mep_prune_table_E, 1, 1496880, file2);
					fclose(file2);

					pattern = 1;
				}

				else if (10 <= pattern && pattern < 14) {

					co_eep_prune_table_E = new unsigned char[8981280];
					co_sep_prune_table_E = new unsigned char[8981280];
					co_mep_prune_table_E = new unsigned char[8981280];
					eo_eep_prune_table_E = new unsigned char[12165120];
					cp_eep_prune_table_E = new unsigned char[1995840];

					FILE* file0;
					fopen_s(&file0, (std::string("Tables\\co_eep-1-2-") + std::to_string(pattern - 10) + std::string(".bin")).c_str(), "rb");
					fread(co_eep_prune_table_E, 1, 8981280, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, (std::string("Tables\\co_sep-1-2-") + std::to_string(pattern - 10) + std::string(".bin")).c_str(), "rb");
					fread(co_sep_prune_table_E, 1, 8981280, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, (std::string("Tables\\co_mep-1-2-") + std::to_string(pattern - 10) + std::string(".bin")).c_str(), "rb");
					fread(co_mep_prune_table_E, 1, 8981280, file2);
					fclose(file2);

					FILE* file3;
					fopen_s(&file3, (std::string("Tables\\eo_eep-1-2-") + std::to_string(pattern - 10) + std::string(".bin")).c_str(), "rb");
					fread(eo_eep_prune_table_E, 1, 12165120, file3);
					fclose(file3);

					FILE* file4;
					fopen_s(&file4, (std::string("Tables\\cp_eep-1-2-") + std::to_string(pattern - 10) + std::string(".bin")).c_str(), "rb");
					fread(cp_eep_prune_table_E, 1, 1995840, file4);
					fclose(file4);

					pattern = 2;
				}

				else if (pattern == 14) {

					co_eep_prune_table_E = new unsigned char[33679800];
					co_sep_prune_table_E = new unsigned char[33679800];
					co_mep_prune_table_E = new unsigned char[33679800];
					eo_eep_prune_table_E = new unsigned char[12165120];
					cp_eep_prune_table_E = new unsigned char[9979200];

					FILE* file0;
					fopen_s(&file0, (std::string("Tables\\co_eep-1-3-") + std::to_string(pattern - 14) + std::string(".bin")).c_str(), "rb");
					fread(co_eep_prune_table_E, 1, 33679800, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, (std::string("Tables\\co_sep-1-3-") + std::to_string(pattern - 14) + std::string(".bin")).c_str(), "rb");
					fread(co_sep_prune_table_E, 1, 33679800, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, (std::string("Tables\\co_mep-1-3-") + std::to_string(pattern - 14) + std::string(".bin")).c_str(), "rb");
					fread(co_mep_prune_table_E, 1, 33679800, file2);
					fclose(file2);

					FILE* file3;
					fopen_s(&file3, (std::string("Tables\\eo_eep-1-3-") + std::to_string(pattern - 14) + std::string(".bin")).c_str(), "rb");
					fread(eo_eep_prune_table_E, 1, 12165120, file3);
					fclose(file3);

					FILE* file4;
					fopen_s(&file4, (std::string("Tables\\cp_eep-1-3-") + std::to_string(pattern - 14) + std::string(".bin")).c_str(), "rb");
					fread(cp_eep_prune_table_E, 1, 9979200, file4);
					fclose(file4);

					pattern = 3;
				}

				for (int i = 47; i < 53; ++i) {
					if (std::stoi(argv[i]) == 1) {
						move_name_index_E.emplace_back(3 * i - 141);
						move_name_index_E.emplace_back(3 * i - 139);
					}
				}

				Search_F2L1 solution(scrambled_state);

				solution.start_search(min_length, max_length, sol_num);
			}
		}

		else {

			center_move_table_E.reserve(24);

			const Value& center_move_tbl = doc1["CENTER_MOVE_TABLE"].GetArray();
			for (auto& d : center_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				center_move_table_E.emplace_back(X);
			}

			std::vector<int> Cpp_cp;
			std::vector<int> Cpp_co;
			std::vector<int> Cpp_ep;
			std::vector<int> Cpp_eo;
			std::vector<int> Cpp_center;
			Cpp_cp.reserve(8);
			Cpp_co.reserve(8);
			Cpp_ep.reserve(12);
			Cpp_eo.reserve(12);
			Cpp_center.reserve(6);

			for (int i = 1; i < 9; ++i) {
				Cpp_cp.emplace_back(std::stoi(argv[i]));
			}

			for (int i = 9; i < 17; ++i) {
				Cpp_co.emplace_back(std::stoi(argv[i]));
			}

			for (int i = 17; i < 29; ++i) {
				Cpp_ep.emplace_back(std::stoi(argv[i]));
			}

			for (int i = 29; i < 41; ++i) {
				Cpp_eo.emplace_back(std::stoi(argv[i]));
			}

			for (int i = 41; i < 47; ++i) {
				Cpp_center.emplace_back(std::stoi(argv[i]));
			}

			int min_length = std::stoi(argv[62]);
			int max_length = std::stoi(argv[63]);
			int sol_num = std::stoi(argv[64]);

			State_fs scrambled_state(Cpp_cp, Cpp_co, Cpp_ep, Cpp_eo, Cpp_center);

			if (std::stoi(argv[65]) == 2) {

				if (pattern < 4) {

					co_mep_prune_table_E = new unsigned char[142560];
					co_sep_prune_table_E = new unsigned char[142560];

					FILE* file0;
					fopen_s(&file0, (std::string("Tables\\co_mep-2-0-") + std::to_string(pattern) + std::string(".bin")).c_str(), "rb");
					fread(co_mep_prune_table_E, 1, 142560, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, (std::string("Tables\\co_sep-2-0-") + std::to_string(pattern) + std::string(".bin")).c_str(), "rb");
					fread(co_sep_prune_table_E, 1, 142560, file1);
					fclose(file1);

					pattern = 0;
				}

				else if (4 <= pattern && pattern < 10) {

					co_eep_prune_table_E = new unsigned char[1496880];
					co_sep_prune_table_E = new unsigned char[1496880];
					co_mep_prune_table_E = new unsigned char[1496880];

					FILE* file0;
					fopen_s(&file0, (std::string("Tables\\co_eep-2-1-") + std::to_string(pattern - 4) + std::string(".bin")).c_str(), "rb");
					fread(co_eep_prune_table_E, 1, 1496880, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, (std::string("Tables\\co_sep-2-1-") + std::to_string(pattern - 4) + std::string(".bin")).c_str(), "rb");
					fread(co_sep_prune_table_E, 1, 1496880, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, (std::string("Tables\\co_mep-2-1-") + std::to_string(pattern - 4) + std::string(".bin")).c_str(), "rb");
					fread(co_mep_prune_table_E, 1, 1496880, file2);
					fclose(file2);

					pattern = 1;
				}

				else if (10 <= pattern && pattern < 14) {

					co_eep_prune_table_E = new unsigned char[8981280];
					co_sep_prune_table_E = new unsigned char[8981280];
					co_mep_prune_table_E = new unsigned char[8981280];
					cp_eep_prune_table_E = new unsigned char[1995840];

					FILE* file0;
					fopen_s(&file0, (std::string("Tables\\co_eep-2-2-") + std::to_string(pattern - 10) + std::string(".bin")).c_str(), "rb");
					fread(co_eep_prune_table_E, 1, 8981280, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, (std::string("Tables\\co_sep-2-2-") + std::to_string(pattern - 10) + std::string(".bin")).c_str(), "rb");
					fread(co_sep_prune_table_E, 1, 8981280, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, (std::string("Tables\\co_mep-2-2-") + std::to_string(pattern - 10) + std::string(".bin")).c_str(), "rb");
					fread(co_mep_prune_table_E, 1, 8981280, file2);
					fclose(file2);

					FILE* file3;
					fopen_s(&file3, (std::string("Tables\\cp_eep-2-2-") + std::to_string(pattern - 10) + std::string(".bin")).c_str(), "rb");
					fread(cp_eep_prune_table_E, 1, 1995840, file3);
					fclose(file3);

					pattern = 2;
				}

				else if (pattern == 14) {

					co_eep_prune_table_E = new unsigned char[33679800];
					co_sep_prune_table_E = new unsigned char[33679800];
					co_mep_prune_table_E = new unsigned char[33679800];
					cp_eep_prune_table_E = new unsigned char[9979200];

					FILE* file0;
					fopen_s(&file0, (std::string("Tables\\co_eep-2-3-") + std::to_string(pattern - 14) + std::string(".bin")).c_str(), "rb");
					fread(co_eep_prune_table_E, 1, 33679800, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, (std::string("Tables\\co_sep-2-3-") + std::to_string(pattern - 14) + std::string(".bin")).c_str(), "rb");
					fread(co_sep_prune_table_E, 1, 33679800, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, (std::string("Tables\\co_mep-2-3-") + std::to_string(pattern - 14) + std::string(".bin")).c_str(), "rb");
					fread(co_mep_prune_table_E, 1, 33679800, file2);
					fclose(file2);

					FILE* file3;
					fopen_s(&file3, (std::string("Tables\\cp_eep-2-3-") + std::to_string(pattern - 14) + std::string(".bin")).c_str(), "rb");
					fread(cp_eep_prune_table_E, 1, 9979200, file3);
					fclose(file3);

					pattern = 3;
				}

				for (int i = 47; i < 62; ++i) {
					if (std::stoi(argv[i]) == 1) {
						move_name_index_E.emplace_back(3 * i - 141);
						move_name_index_E.emplace_back(3 * i - 140);
						move_name_index_E.emplace_back(3 * i - 139);
					}
				}

				Search_F2L2 solution(scrambled_state);

				solution.start_search_fs(min_length, max_length, sol_num);
			}

			else if (std::stoi(argv[65]) == 3) {

				if (pattern < 4) {

					co_mep_prune_table_E = new unsigned char[142560];
					co_sep_prune_table_E = new unsigned char[142560];

					FILE* file0;
					fopen_s(&file0, (std::string("Tables\\co_mep-3-0-") + std::to_string(pattern) + std::string(".bin")).c_str(), "rb");
					fread(co_mep_prune_table_E, 1, 142560, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, (std::string("Tables\\co_sep-3-0-") + std::to_string(pattern) + std::string(".bin")).c_str(), "rb");
					fread(co_sep_prune_table_E, 1, 142560, file1);
					fclose(file1);

					pattern = 0;
				}

				else if (4 <= pattern && pattern < 10) {

					co_eep_prune_table_E = new unsigned char[1496880];
					co_sep_prune_table_E = new unsigned char[1496880];
					co_mep_prune_table_E = new unsigned char[1496880];

					FILE* file0;
					fopen_s(&file0, (std::string("Tables\\co_eep-3-1-") + std::to_string(pattern - 4) + std::string(".bin")).c_str(), "rb");
					fread(co_eep_prune_table_E, 1, 1496880, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, (std::string("Tables\\co_sep-3-1-") + std::to_string(pattern - 4) + std::string(".bin")).c_str(), "rb");
					fread(co_sep_prune_table_E, 1, 1496880, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, (std::string("Tables\\co_mep-3-1-") + std::to_string(pattern - 4) + std::string(".bin")).c_str(), "rb");
					fread(co_mep_prune_table_E, 1, 1496880, file2);
					fclose(file2);

					pattern = 1;
				}

				else if (10 <= pattern && pattern < 14) {

					co_eep_prune_table_E = new unsigned char[8981280];
					co_sep_prune_table_E = new unsigned char[8981280];
					co_mep_prune_table_E = new unsigned char[8981280];
					cp_eep_prune_table_E = new unsigned char[1995840];

					FILE* file0;
					fopen_s(&file0, (std::string("Tables\\co_eep-3-2-") + std::to_string(pattern - 10) + std::string(".bin")).c_str(), "rb");
					fread(co_eep_prune_table_E, 1, 8981280, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, (std::string("Tables\\co_sep-3-2-") + std::to_string(pattern - 10) + std::string(".bin")).c_str(), "rb");
					fread(co_sep_prune_table_E, 1, 8981280, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, (std::string("Tables\\co_mep-3-2-") + std::to_string(pattern - 10) + std::string(".bin")).c_str(), "rb");
					fread(co_mep_prune_table_E, 1, 8981280, file2);
					fclose(file2);

					FILE* file3;
					fopen_s(&file3, (std::string("Tables\\cp_eep-3-2-") + std::to_string(pattern - 10) + std::string(".bin")).c_str(), "rb");
					fread(cp_eep_prune_table_E, 1, 1995840, file3);
					fclose(file3);

					pattern = 2;
				}

				else if (pattern == 14) {

					co_eep_prune_table_E = new unsigned char[33679800];
					co_sep_prune_table_E = new unsigned char[33679800];
					co_mep_prune_table_E = new unsigned char[33679800];
					cp_eep_prune_table_E = new unsigned char[9979200];

					FILE* file0;
					fopen_s(&file0, (std::string("Tables\\co_eep-3-3-") + std::to_string(pattern - 14) + std::string(".bin")).c_str(), "rb");
					fread(co_eep_prune_table_E, 1, 33679800, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, (std::string("Tables\\co_sep-3-3-") + std::to_string(pattern - 14) + std::string(".bin")).c_str(), "rb");
					fread(co_sep_prune_table_E, 1, 33679800, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, (std::string("Tables\\co_mep-3-3-") + std::to_string(pattern - 14) + std::string(".bin")).c_str(), "rb");
					fread(co_mep_prune_table_E, 1, 33679800, file2);
					fclose(file2);

					FILE* file4;
					fopen_s(&file4, (std::string("Tables\\cp_eep-3-3-") + std::to_string(pattern - 14) + std::string(".bin")).c_str(), "rb");
					fread(cp_eep_prune_table_E, 1, 9979200, file4);
					fclose(file4);

					pattern = 3;
				}

				for (int i = 47; i < 62; ++i) {
					if (std::stoi(argv[i]) == 1) {
						move_name_index_E.emplace_back(3 * i - 141);
						move_name_index_E.emplace_back(3 * i - 139);
					}
				}

				Search_F2L3 solution(scrambled_state);

				solution.start_search_fs(min_length, max_length, sol_num);
			}
		}
	}

	else if (argc == 69) {

		forbidden = std::stoi(argv[66]);
		brackets = std::stoi(argv[67]);

		std::ifstream ifs("pre_culculation_E.json");
		IStreamWrapper isw(ifs);
		Document doc;
		doc.ParseStream(isw);

		co_move_table_E.reserve(2187);

		const Value& co_move_tbl = doc["CO_MOVE_TABLE"].GetArray();
		for (auto& d : co_move_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(45);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			co_move_table_E.emplace_back(X);
		}

		eo_move_table_E.reserve(2048);

		const Value& eo_move_tbl = doc["EO_MOVE_TABLE"].GetArray();
		for (auto& d : eo_move_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(45);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			eo_move_table_E.emplace_back(X);
		}

		ep_move_table_E.reserve(11880);

		const Value& ep_move_tbl = doc["EP_MOVE_TABLE"].GetArray();
		for (auto& d : ep_move_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(45);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			ep_move_table_E.emplace_back(X);
		}

		if (std::stoi(argv[68]) == 0) {
			cp_move_table_E.reserve(40320);

			const Value& cp_move_tbl = doc["CP_MOVE_TABLE"].GetArray();
			for (auto& d : cp_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				cp_move_table_E.emplace_back(X);
			}

			if (std::stoi(argv[65]) == 0 || std::stoi(argv[65]) == 1) {

				std::vector<int> Cpp_cp;
				std::vector<int> Cpp_co;
				std::vector<int> Cpp_ep;
				std::vector<int> Cpp_eo;
				Cpp_cp.reserve(8);
				Cpp_co.reserve(8);
				Cpp_ep.reserve(12);
				Cpp_eo.reserve(12);

				for (int i = 1; i < 9; ++i) {
					Cpp_cp.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 9; i < 17; ++i) {
					Cpp_co.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 17; i < 29; ++i) {
					Cpp_ep.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 29; i < 41; ++i) {
					Cpp_eo.emplace_back(std::stoi(argv[i]));
				}

				int min_length = std::stoi(argv[62]);
				int max_length = std::stoi(argv[63]);
				int sol_num = std::stoi(argv[64]);

				State scrambled_state(Cpp_cp, Cpp_co, Cpp_ep, Cpp_eo);

				if (std::stoi(argv[65]) == 0) {

					co_cp_prune_table_E = new unsigned char[44089920];
					cp_mep_prune_table_E = new unsigned char[239500800];
					cp_eep_prune_table_E = new unsigned char[239500800];
					cp_sep_prune_table_E = new unsigned char[239500800];

					FILE* file0;
					fopen_s(&file0, "Tables\\co_cp0.bin", "rb");
					fread(co_cp_prune_table_E, 1, 44089920, file0);
					fclose(file0);

					FILE* file4;
					fopen_s(&file4, "Tables\\cp_mep0.bin", "rb");
					fread(cp_mep_prune_table_E, 1, 239500800, file4);
					fclose(file4);

					FILE* file5;
					fopen_s(&file5, "Tables\\cp_eep0.bin", "rb");
					fread(cp_eep_prune_table_E, 1, 239500800, file5);
					fclose(file5);

					FILE* file6;
					fopen_s(&file6, "Tables\\cp_sep0.bin", "rb");
					fread(cp_sep_prune_table_E, 1, 239500800, file6);
					fclose(file6);

					for (int i = 47; i < 53; ++i) {
						if (std::stoi(argv[i]) == 1) {
							move_name_index_E.emplace_back(3 * i - 141);
							move_name_index_E.emplace_back(3 * i - 140);
							move_name_index_E.emplace_back(3 * i - 139);
						}
					}

					Search_PLL0 solution(scrambled_state);

					solution.start_search(min_length, max_length, sol_num);
				}

				else if (std::stoi(argv[65]) == 1) {

					co_cp_prune_table_E = new unsigned char[44089920];
					cp_mep_prune_table_E = new unsigned char[239500800];
					cp_eep_prune_table_E = new unsigned char[239500800];
					cp_sep_prune_table_E = new unsigned char[239500800];

					FILE* file0;
					fopen_s(&file0, "Tables\\co_cp1.bin", "rb");
					fread(co_cp_prune_table_E, 1, 44089920, file0);
					fclose(file0);

					FILE* file4;
					fopen_s(&file4, "Tables\\cp_mep1.bin", "rb");
					fread(cp_mep_prune_table_E, 1, 239500800, file4);
					fclose(file4);

					FILE* file5;
					fopen_s(&file5, "Tables\\cp_eep1.bin", "rb");
					fread(cp_eep_prune_table_E, 1, 239500800, file5);
					fclose(file5);

					FILE* file6;
					fopen_s(&file6, "Tables\\cp_sep1.bin", "rb");
					fread(cp_sep_prune_table_E, 1, 239500800, file6);
					fclose(file6);

					for (int i = 47; i < 53; ++i) {
						if (std::stoi(argv[i]) == 1) {
							move_name_index_E.emplace_back(3 * i - 141);
							move_name_index_E.emplace_back(3 * i - 139);
						}
					}

					Search_PLL1 solution(scrambled_state);

					solution.start_search(min_length, max_length, sol_num);
				}
			}

			else {
				
				center_move_table_E.reserve(24);

				const Value& center_move_tbl = doc["CENTER_MOVE_TABLE"].GetArray();
				for (auto& d : center_move_tbl.GetArray()) {
					//const auto e = d.GetArray();
					std::vector<int> X;
					X.reserve(45);
					for (auto& f : d.GetArray()) {
						//int i = 0;
						const int g = f.GetInt();
						X.emplace_back(g);
						//++i;
					}
					center_move_table_E.emplace_back(X);
				}

				std::vector<int> Cpp_cp;
				std::vector<int> Cpp_co;
				std::vector<int> Cpp_ep;
				std::vector<int> Cpp_eo;
				std::vector<int> Cpp_center;
				Cpp_cp.reserve(8);
				Cpp_co.reserve(8);
				Cpp_ep.reserve(12);
				Cpp_eo.reserve(12);
				Cpp_center.reserve(6);

				for (int i = 1; i < 9; ++i) {
					Cpp_cp.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 9; i < 17; ++i) {
					Cpp_co.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 17; i < 29; ++i) {
					Cpp_ep.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 29; i < 41; ++i) {
					Cpp_eo.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 41; i < 47; ++i) {
					Cpp_center.emplace_back(std::stoi(argv[i]));
				}

				int min_length = std::stoi(argv[62]);
				int max_length = std::stoi(argv[63]);
				int sol_num = std::stoi(argv[64]);

				State_fs scrambled_state(Cpp_cp, Cpp_co, Cpp_ep, Cpp_eo, Cpp_center);

				if (std::stoi(argv[65]) == 2) {

					co_cp_prune_table_E = new unsigned char[44089920];
					cp_mep_prune_table_E = new unsigned char[239500800];
					co_eo_center_prune_table_E = new unsigned char[53747712];

					FILE* file0;
					fopen_s(&file0, "Tables\\co_cp2.bin", "rb");
					fread(co_cp_prune_table_E, 1, 44089920, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, "Tables\\cp_mep2.bin", "rb");
					fread(cp_mep_prune_table_E, 1, 44089920, file1);
					fclose(file1);

					FILE* file4;
					fopen_s(&file4, "Tables\\co_eo_center2.bin", "rb");
					fread(co_eo_center_prune_table_E, 1, 53747712, file4);
					fclose(file4);

					for (int i = 47; i < 62; ++i) {
						if (std::stoi(argv[i]) == 1) {
							move_name_index_E.emplace_back(3 * i - 141);
							move_name_index_E.emplace_back(3 * i - 140);
							move_name_index_E.emplace_back(3 * i - 139);
						}
					}

					Search_PLL2 solution(scrambled_state);

					solution.start_search_fs(min_length, max_length, sol_num);
				}

				else if (std::stoi(argv[65]) == 3) {

					co_cp_prune_table_E = new unsigned char[44089920];
					co_eo_center_prune_table_E = new unsigned char[53747712];

					FILE* file0;
					fopen_s(&file0, "Tables\\co_cp3.bin", "rb");
					fread(co_cp_prune_table_E, 1, 44089920, file0);
					fclose(file0);

					FILE* file4;
					fopen_s(&file4, "Tables\\co_eo_center3.bin", "rb");
					fread(co_eo_center_prune_table_E, 1, 53747712, file4);
					fclose(file4);

					for (int i = 47; i < 62; ++i) {
						if (std::stoi(argv[i]) == 1) {
							move_name_index_E.emplace_back(3 * i - 141);
							move_name_index_E.emplace_back(3 * i - 139);
						}
					}

					Search_PLL3 solution(scrambled_state);

					solution.start_search_fs(min_length, max_length, sol_num);
				}
			}
		}

		else if (std::stoi(argv[68]) == 1) {
			cp_move_table_E.reserve(1680);

			const Value& OLL_cp_move_tbl = doc["OLL_CP_MOVE_TABLE"].GetArray();
			for (auto& d : OLL_cp_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				cp_move_table_E.emplace_back(X);
			}

			if (std::stoi(argv[65]) == 0 || std::stoi(argv[65]) == 1) {

				std::vector<int> Cpp_cp;
				std::vector<int> Cpp_co;
				std::vector<int> Cpp_ep;
				std::vector<int> Cpp_eo;
				Cpp_cp.reserve(8);
				Cpp_co.reserve(8);
				Cpp_ep.reserve(12);
				Cpp_eo.reserve(12);

				std::vector<std::vector<int>> gen = { { 0, 1, 2 }, { 3, 4, 5 }, { 6, 7, 8 }, { 9, 10, 11 }, { 12, 13, 14 }, { 15, 16, 17 } };

				for (int i = 1; i < 9; ++i) {
					Cpp_cp.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 9; i < 17; ++i) {
					Cpp_co.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 17; i < 29; ++i) {
					Cpp_ep.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 29; i < 41; ++i) {
					Cpp_eo.emplace_back(std::stoi(argv[i]));
				}

				int min_length = std::stoi(argv[62]);
				int max_length = std::stoi(argv[63]);
				int sol_num = std::stoi(argv[64]);

				State scrambled_state(Cpp_cp, Cpp_co, Cpp_ep, Cpp_eo);

				if (std::stoi(argv[65]) == 0) {

					co_cp_prune_table_E = new unsigned char[1837080];
					co_eep_prune_table_E = new unsigned char[12990780];
					co_eo_prune_table_E = new unsigned char[2239488];
					eo_eep_prune_table_E = new unsigned char[12165120];

					FILE* file0;
					fopen_s(&file0, "Tables\\OLL_co_cp0.bin", "rb");
					fread(co_cp_prune_table_E, 1, 1837080, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, "Tables\\OLL_co_eep0.bin", "rb");
					fread(co_eep_prune_table_E, 1, 12990780, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, "Tables\\OLL_co_eo0.bin", "rb");
					fread(co_eo_prune_table_E, 1, 2239488, file2);
					fclose(file2);

					FILE* file5;
					fopen_s(&file5, "Tables\\OLL_eo_eep0.bin", "rb");
					fread(eo_eep_prune_table_E, 1, 12165120, file5);
					fclose(file5);

					if (forbidden == 0) {
						x_rotation_move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'", "R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" };
						for (int i = 47; i < 53; ++i) {
							if (std::stoi(argv[i]) == 1) {
								move_name_index_E.emplace_back(3 * i - 141);
								move_name_index_E.emplace_back(3 * i - 140);
								move_name_index_E.emplace_back(3 * i - 139);
							}
						}
					}

					else if (forbidden == 15) {
						x_rotation_move_names = { "B", "B2", "B'", "F", "F2", "F'", "L", "L2", "L'", "R", "R2", "R'", "U", "U2", "U'", "D", "D2", "D'" };
						for (int i = 47; i < 53; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), gen[4].begin(), gen[4].end());
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), gen[5].begin(), gen[5].end());
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), gen[2].begin(), gen[2].end());
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), gen[3].begin(), gen[3].end());
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), gen[1].begin(), gen[1].end());
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), gen[0].begin(), gen[0].end());
								}
							}
						}
					}

					else if (forbidden == 12) {
						x_rotation_move_names = { "F", "F2", "F'", "B", "B2", "B'", "L", "L2", "L'", "R", "R2", "R'", "D", "D2", "D'", "U", "U2", "U'" };
						for (int i = 47; i < 53; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), gen[5].begin(), gen[5].end());
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), gen[4].begin(), gen[4].end());
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), gen[2].begin(), gen[2].end());
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), gen[3].begin(), gen[3].end());
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), gen[0].begin(), gen[0].end());
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), gen[1].begin(), gen[1].end());
								}
							}
						}
					}

					Search_OLL0 solution(scrambled_state);

					solution.start_search(min_length, max_length, sol_num);
				}

				else if (std::stoi(argv[65]) == 1) {
					
					co_cp_prune_table_E = new unsigned char[1837080];
					co_eep_prune_table_E = new unsigned char[12990780];
					co_eo_prune_table_E = new unsigned char[2239488];
					eo_eep_prune_table_E = new unsigned char[12165120];

					FILE* file0;
					fopen_s(&file0, "Tables\\OLL_co_cp1.bin", "rb");
					fread(co_cp_prune_table_E, 1, 1837080, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, "Tables\\OLL_co_eep1.bin", "rb");
					fread(co_eep_prune_table_E, 1, 12990780, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, "Tables\\OLL_co_eo1.bin", "rb");
					fread(co_eo_prune_table_E, 1, 2239488, file2);
					fclose(file2);

					FILE* file4;
					fopen_s(&file4, "Tables\\OLL_eo_eep1.bin", "rb");
					fread(eo_eep_prune_table_E, 1, 12165120, file4);
					fclose(file4);

					if (forbidden == 0) {
						x_rotation_move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'", "R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" };
						for (int i = 47; i < 53; ++i) {
							if (std::stoi(argv[i]) == 1) {
								move_name_index_E.emplace_back(3 * i - 141);
								move_name_index_E.emplace_back(3 * i - 139);
							}
						}
					}

					else if (forbidden == 15) {
						x_rotation_move_names = { "B", "B2", "B'", "F", "F2", "F'", "L", "L2", "L'", "R", "R2", "R'", "U", "U2", "U'", "D", "D2", "D'" };
						for (int i = 47; i < 53; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[4][0], gen[4][2] });
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[5][0], gen[5][2] });
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[2][0], gen[2][2] });
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[3][0], gen[3][2] });
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[1][0], gen[1][2] });
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[0][0], gen[0][2] });
								}
							}
						}
					}

					else if (forbidden == 12) {
						x_rotation_move_names = { "F", "F2", "F'", "B", "B2", "B'", "L", "L2", "L'", "R", "R2", "R'", "D", "D2", "D'", "U", "U2", "U'" };
						for (int i = 47; i < 53; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[5][0], gen[5][2] });
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[4][0], gen[4][2] });
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[2][0], gen[2][2] });
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[3][0], gen[3][2] });
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[1][0], gen[1][2] });
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[1][0], gen[1][2] });
								}
							}
						}
					}

					Search_OLL1 solution(scrambled_state);

					solution.start_search(min_length, max_length, sol_num);
				}
			}

			else {

				center_move_table_E.reserve(24);

				const Value& center_move_tbl = doc["CENTER_MOVE_TABLE"].GetArray();
				for (auto& d : center_move_tbl.GetArray()) {
					//const auto e = d.GetArray();
					std::vector<int> X;
					X.reserve(45);
					for (auto& f : d.GetArray()) {
						//int i = 0;
						const int g = f.GetInt();
						X.emplace_back(g);
						//++i;
					}
					center_move_table_E.emplace_back(X);
				}

				std::vector<int> Cpp_cp;
				std::vector<int> Cpp_co;
				std::vector<int> Cpp_ep;
				std::vector<int> Cpp_eo;
				std::vector<int> Cpp_center;
				Cpp_cp.reserve(8);
				Cpp_co.reserve(8);
				Cpp_ep.reserve(12);
				Cpp_eo.reserve(12);
				Cpp_center.reserve(6);

				std::vector<std::vector<int>> gen = { { 0, 1, 2 }, { 3, 4, 5 }, { 6, 7, 8 }, { 9, 10, 11 }, { 12, 13, 14 }, { 15, 16, 17 }, { 18, 19, 20 }, { 21, 22, 23 }, { 24, 25, 26 }, { 27, 28, 29 }, { 30, 31, 32 }, { 33, 34, 35 }, { 36, 37, 38 }, { 39, 40, 41 }, { 42, 43, 44 } };

				for (int i = 1; i < 9; ++i) {
					Cpp_cp.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 9; i < 17; ++i) {
					Cpp_co.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 17; i < 29; ++i) {
					Cpp_ep.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 29; i < 41; ++i) {
					Cpp_eo.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 41; i < 47; ++i) {
					Cpp_center.emplace_back(std::stoi(argv[i]));
				}

				int min_length = std::stoi(argv[62]);
				int max_length = std::stoi(argv[63]);
				int sol_num = std::stoi(argv[64]);

				State_fs scrambled_state(Cpp_cp, Cpp_co, Cpp_ep, Cpp_eo, Cpp_center);

				if (std::stoi(argv[65]) == 2) {

					co_cp_prune_table_E = new unsigned char[1837080];
					co_eep_prune_table_E = new unsigned char[12990780];
					eo_eep_prune_table_E = new unsigned char[12165120];
					co_eo_center_prune_table_E = new unsigned char[53747712];
					cp_eep_center_prune_table_E = new unsigned char[239500800];

					FILE* file0;
					fopen_s(&file0, "Tables\\OLL_co_cp2.bin", "rb");
					fread(co_cp_prune_table_E, 1, 1837080, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, "Tables\\OLL_co_eep2.bin", "rb");
					fread(co_eep_prune_table_E, 1, 9979200, file1);
					fclose(file1);

					FILE* file3;
					fopen_s(&file3, "Tables\\OLL_eo_eep2.bin", "rb");
					fread(eo_eep_prune_table_E, 1, 12165120, file3);
					fclose(file3);

					FILE* file4;
					fopen_s(&file4, "Tables\\co_eo_center2.bin", "rb");
					fread(co_eo_center_prune_table_E, 1, 53747712, file4);
					fclose(file4);

					FILE* file5;
					fopen_s(&file5, "Tables\\OLL_cp_eep_center2.bin", "rb");
					fread(cp_eep_center_prune_table_E, 1, 239500800, file5);
					fclose(file5);

					if (forbidden == 0) {
						x_rotation_move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'", "R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'", "Uw", "Uw2", "Uw'", "Dw", "Dw2", "Dw'", "Lw", "Lw2", "Lw'", "Rw", "Rw2", "Rw'", "Fw", "Fw2", "Fw'", "Bw", "Bw2", "Bw'", "M", "M2", "M'", "E", "E2", "E'", "S", "S2", "S'" };
						for (int i = 47; i < 62; ++i) {
							if (std::stoi(argv[i]) == 1) {
								move_name_index_E.emplace_back(3 * i - 141);
								move_name_index_E.emplace_back(3 * i - 140);
								move_name_index_E.emplace_back(3 * i - 139);
							}
						}
					}

					else if (forbidden == 15) {
						x_rotation_move_names = { "B", "B2", "B'", "F", "F2", "F'", "L", "L2", "L'", "R", "R2", "R'", "U", "U2", "U'", "D", "D2", "D'", "Bw", "Bw2", "Bw'", "Fw", "Fw2", "Fw'", "Lw", "Lw2", "Lw'", "Rw", "Rw2", "Rw'", "Uw", "Uw2", "Uw'", "Dw", "Dw2", "Dw'", "M", "M2", "M'", "S", "S2", "S'", "E", "E2", "E'" };
						for (int i = 47; i < 62; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), gen[4].begin(), gen[4].end());
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), gen[5].begin(), gen[5].end());
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), gen[2].begin(), gen[2].end());
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), gen[3].begin(), gen[3].end());
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), gen[1].begin(), gen[1].end());
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), gen[0].begin(), gen[0].end());
								}
								else if (i == 53) {
									move_name_index_E.insert(move_name_index_E.end(), gen[10].begin(), gen[10].end());
								}
								else if (i == 54) {
									move_name_index_E.insert(move_name_index_E.end(), gen[11].begin(), gen[11].end());
								}
								else if (i == 55) {
									move_name_index_E.insert(move_name_index_E.end(), gen[8].begin(), gen[8].end());
								}
								else if (i == 56) {
									move_name_index_E.insert(move_name_index_E.end(), gen[9].begin(), gen[9].end());
								}
								else if (i == 57) {
									move_name_index_E.insert(move_name_index_E.end(), gen[7].begin(), gen[7].end());
								}
								else if (i == 58) {
									move_name_index_E.insert(move_name_index_E.end(), gen[6].begin(), gen[6].end());
								}
								else if (i == 59) {
									move_name_index_E.insert(move_name_index_E.end(), gen[12].begin(), gen[12].end());
								}
								else if (i == 60) {
									move_name_index_E.insert(move_name_index_E.end(), gen[14].begin(), gen[14].end());
								}
								else if (i == 61) {
									move_name_index_E.insert(move_name_index_E.end(), gen[13].begin(), gen[13].end());
								}
							}
						}
					}

					else if (forbidden == 12) {
						x_rotation_move_names = { "F", "F2", "F'", "B", "B2", "B'", "L", "L2", "L'", "R", "R2", "R'", "D", "D2", "D'", "U", "U2", "U'", "Fw", "Fw2", "Fw'", "Bw", "Bw2", "Bw'", "Lw", "Lw2", "Lw'", "Rw", "Rw2", "Rw'", "Dw", "Dw2", "Dw'", "Uw", "Uw2", "Uw'", "M", "M2", "M'", "S", "S2", "S'", "E", "E2", "E'" };
						for (int i = 47; i < 62; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), gen[5].begin(), gen[5].end());
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), gen[4].begin(), gen[4].end());
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), gen[2].begin(), gen[2].end());
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), gen[3].begin(), gen[3].end());
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), gen[0].begin(), gen[0].end());
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), gen[1].begin(), gen[1].end());
								}
								else if (i == 53) {
									move_name_index_E.insert(move_name_index_E.end(), gen[11].begin(), gen[11].end());
								}
								else if (i == 54) {
									move_name_index_E.insert(move_name_index_E.end(), gen[10].begin(), gen[10].end());
								}
								else if (i == 55) {
									move_name_index_E.insert(move_name_index_E.end(), gen[8].begin(), gen[8].end());
								}
								else if (i == 56) {
									move_name_index_E.insert(move_name_index_E.end(), gen[9].begin(), gen[9].end());
								}
								else if (i == 57) {
									move_name_index_E.insert(move_name_index_E.end(), gen[6].begin(), gen[6].end());
								}
								else if (i == 58) {
									move_name_index_E.insert(move_name_index_E.end(), gen[7].begin(), gen[7].end());
								}
								else if (i == 59) {
									move_name_index_E.insert(move_name_index_E.end(), gen[12].begin(), gen[12].end());
								}
								else if (i == 60) {
									move_name_index_E.insert(move_name_index_E.end(), gen[14].begin(), gen[14].end());
								}
								else if (i == 61) {
									move_name_index_E.insert(move_name_index_E.end(), gen[13].begin(), gen[13].end());
								}
							}
						}
					}

					Search_OLL2 solution(scrambled_state);

					solution.start_search_fs(min_length, max_length, sol_num);
				}

				else if (std::stoi(argv[65]) == 3) {
					
					co_cp_prune_table_E = new unsigned char[1837080];
					co_eep_prune_table_E = new unsigned char[12990780];
					cp_eep_prune_table_E = new unsigned char[9979200];
					co_eo_center_prune_table_E = new unsigned char[53747712];

					FILE* file0;
					fopen_s(&file0, "Tables\\OLL_co_cp3.bin", "rb");
					fread(co_cp_prune_table_E, 1, 1837080, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, "Tables\\OLL_co_eep3.bin", "rb");
					fread(co_eep_prune_table_E, 1, 12990780, file1);
					fclose(file1);

					FILE* file3;
					fopen_s(&file3, "Tables\\OLL_cp_eep3.bin", "rb");
					fread(cp_eep_prune_table_E, 1, 9979200, file3);
					fclose(file3);

					FILE* file4;
					fopen_s(&file4, "Tables\\co_eo_center3.bin", "rb");
					fread(co_eo_center_prune_table_E, 1, 53747712, file4);
					fclose(file4);

					if (forbidden == 0) {
						x_rotation_move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'", "R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'", "Uw", "Uw2", "Uw'", "Dw", "Dw2", "Dw'", "Lw", "Lw2", "Lw'", "Rw", "Rw2", "Rw'", "Fw", "Fw2", "Fw'", "Bw", "Bw2", "Bw'", "M", "M2", "M'", "E", "E2", "E'", "S", "S2", "S'" };
						for (int i = 47; i < 62; ++i) {
							if (std::stoi(argv[i]) == 1) {
								move_name_index_E.emplace_back(3 * i - 141);
								move_name_index_E.emplace_back(3 * i - 139);
							}
						}
					}

					else if (forbidden == 15) {
						x_rotation_move_names = { "B", "B2", "B'", "F", "F2", "F'", "L", "L2", "L'", "R", "R2", "R'", "U", "U2", "U'", "D", "D2", "D'", "Bw", "Bw2", "Bw'", "Fw", "Fw2", "Fw'", "Lw", "Lw2", "Lw'", "Rw", "Rw2", "Rw'", "Uw", "Uw2", "Uw'", "Dw", "Dw2", "Dw'", "M", "M2", "M'", "S", "S2", "S'", "E", "E2", "E'" };
						for (int i = 47; i < 62; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[4][0], gen[4][2] });
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[5][0], gen[5][2] });
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[2][0], gen[2][2] });
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[3][0], gen[3][2] });
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[1][0], gen[1][2] });
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[0][0], gen[0][2] });
								}
								else if (i == 53) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[10][0], gen[10][2] });
								}
								else if (i == 54) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[11][0], gen[11][2] });
								}
								else if (i == 55) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[8][0], gen[8][2] });
								}
								else if (i == 56) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[9][0], gen[9][2] });
								}
								else if (i == 57) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[7][0], gen[7][2] });
								}
								else if (i == 58) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[6][0], gen[6][2] });
								}
								else if (i == 59) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[12][0], gen[12][2] });
								}
								else if (i == 60) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[14][0], gen[14][2] });
								}
								else if (i == 61) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[13][0], gen[13][2] });
								}
							}
						}
					}

					else if (forbidden == 12) {
						x_rotation_move_names = { "F", "F2", "F'", "B", "B2", "B'", "L", "L2", "L'", "R", "R2", "R'", "D", "D2", "D'", "U", "U2", "U'", "Fw", "Fw2", "Fw'", "Bw", "Bw2", "Bw'", "Lw", "Lw2", "Lw'", "Rw", "Rw2", "Rw'", "Dw", "Dw2", "Dw'", "Uw", "Uw2", "Uw'", "M", "M2", "M'", "S", "S2", "S'", "E", "E2", "E'" };
						for (int i = 47; i < 62; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[5][0], gen[5][2] });
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[4][0], gen[4][2] });
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[2][0], gen[2][2] });
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[3][0], gen[3][2] });
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[0][0], gen[0][2] });
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[1][0], gen[1][2] });
								}
								else if (i == 53) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[11][0], gen[11][2] });
								}
								else if (i == 54) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[10][0], gen[10][2] });
								}
								else if (i == 55) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[8][0], gen[8][2] });
								}
								else if (i == 56) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[9][0], gen[9][2] });
								}
								else if (i == 57) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[6][0], gen[6][2] });
								}
								else if (i == 58) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[7][0], gen[7][2] });
								}
								else if (i == 59) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[12][0], gen[12][2] });
								}
								else if (i == 60) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[14][0], gen[14][2] });
								}
								else if (i == 61) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[13][0], gen[13][2] });
								}
							}
						}
					}

					Search_OLL3 solution(scrambled_state);

					solution.start_search_fs(min_length, max_length, sol_num);
				}
			}
		}
	}

	else if (argc == 70) {
		pattern = std::stoi(argv[68]);
		forbidden = std::stoi(argv[66]);
		brackets = std::stoi(argv[67]);

		solved_co = solved_index1["co"][14];
		solved_cp = solved_index1["cp"][14];
		solved_mep = solved_index2["mep"][14];
		solved_eep = solved_index2["eep"][14];
		solved_sep = solved_index2["sep"][14];

		std::ifstream ifs1("pre_culculation_E.json");
		IStreamWrapper isw1(ifs1);
		Document doc1;
		doc1.ParseStream(isw1);

		eo_move_table_E.reserve(2048);

		const Value& eo_move_tbl = doc1["EO_MOVE_TABLE"].GetArray();
		for (auto& d : eo_move_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(45);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			eo_move_table_E.emplace_back(X);
		}

		ep_move_table_E.reserve(11880);

		const Value& ep_move_tbl = doc1["EP_MOVE_TABLE"].GetArray();
		for (auto& d : ep_move_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(45);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			ep_move_table_E.emplace_back(X);
		}

		if (pattern == 0) {
			co_move_table_E.reserve(2187);

			const Value& co_move_tbl = doc1["CO_MOVE_TABLE"].GetArray();
			for (auto& d : co_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				co_move_table_E.emplace_back(X);
			}

			cp_move_table_E.reserve(40320);

			const Value& cp_move_tbl = doc1["CP_MOVE_TABLE"].GetArray();
			for (auto& d : cp_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				cp_move_table_E.emplace_back(X);
			}

			if (std::stoi(argv[65]) == 0 || std::stoi(argv[65]) == 1) {

				std::vector<int> Cpp_cp;
				std::vector<int> Cpp_co;
				std::vector<int> Cpp_ep;
				std::vector<int> Cpp_eo;
				Cpp_cp.reserve(8);
				Cpp_co.reserve(8);
				Cpp_ep.reserve(12);
				Cpp_eo.reserve(12);

				std::vector<std::vector<int>> gen = { { 0, 1, 2 }, { 3, 4, 5 }, { 6, 7, 8 }, { 9, 10, 11 }, { 12, 13, 14 }, { 15, 16, 17 } };

				for (int i = 1; i < 9; ++i) {
					Cpp_cp.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 9; i < 17; ++i) {
					Cpp_co.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 17; i < 29; ++i) {
					Cpp_ep.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 29; i < 41; ++i) {
					Cpp_eo.emplace_back(std::stoi(argv[i]));
				}

				int min_length = std::stoi(argv[62]);
				int max_length = std::stoi(argv[63]);
				int sol_num = std::stoi(argv[64]);

				State scrambled_state(Cpp_cp, Cpp_co, Cpp_ep, Cpp_eo);

				if (std::stoi(argv[65]) == 0) {

					co_cp_prune_table_E = new unsigned char[44089920];
					cp_mep_prune_table_E = new unsigned char[239500800];
					cp_eep_prune_table_E = new unsigned char[239500800];
					cp_sep_prune_table_E = new unsigned char[239500800];

					FILE* file0;
					fopen_s(&file0, "Tables\\co_cp0.bin", "rb");
					fread(co_cp_prune_table_E, 1, 44089920, file0);
					fclose(file0);

					FILE* file4;
					fopen_s(&file4, "Tables\\cp_mep0.bin", "rb");
					fread(cp_mep_prune_table_E, 1, 239500800, file4);
					fclose(file4);

					FILE* file5;
					fopen_s(&file5, "Tables\\cp_eep0.bin", "rb");
					fread(cp_eep_prune_table_E, 1, 239500800, file5);
					fclose(file5);

					FILE* file6;
					fopen_s(&file6, "Tables\\cp_sep0.bin", "rb");
					fread(cp_sep_prune_table_E, 1, 239500800, file6);
					fclose(file6);

					if (forbidden == 0) {
						x_rotation_move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'", "R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" };
						for (int i = 47; i < 53; ++i) {
							if (std::stoi(argv[i]) == 1) {
								move_name_index_E.emplace_back(3 * i - 141);
								move_name_index_E.emplace_back(3 * i - 140);
								move_name_index_E.emplace_back(3 * i - 139);
							}
						}
					}

					else if (forbidden == 15) {
						x_rotation_move_names = { "B", "B2", "B'", "F", "F2", "F'", "L", "L2", "L'", "R", "R2", "R'", "U", "U2", "U'", "D", "D2", "D'" };
						for (int i = 47; i < 53; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), gen[4].begin(), gen[4].end());
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), gen[5].begin(), gen[5].end());
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), gen[2].begin(), gen[2].end());
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), gen[3].begin(), gen[3].end());
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), gen[1].begin(), gen[1].end());
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), gen[0].begin(), gen[0].end());
								}
							}
						}
					}

					else if (forbidden == 12) {
						x_rotation_move_names = { "F", "F2", "F'", "B", "B2", "B'", "L", "L2", "L'", "R", "R2", "R'", "D", "D2", "D'", "U", "U2", "U'" };
						for (int i = 47; i < 53; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), gen[5].begin(), gen[5].end());
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), gen[4].begin(), gen[4].end());
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), gen[2].begin(), gen[2].end());
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), gen[3].begin(), gen[3].end());
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), gen[0].begin(), gen[0].end());
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), gen[1].begin(), gen[1].end());
								}
							}
						}
					}

					Search_PLL0 solution(scrambled_state);

					solution.start_search(min_length, max_length, sol_num);
				}

				else if (std::stoi(argv[65]) == 1) {

					co_cp_prune_table_E = new unsigned char[44089920];
					cp_mep_prune_table_E = new unsigned char[239500800];
					cp_eep_prune_table_E = new unsigned char[239500800];
					cp_sep_prune_table_E = new unsigned char[239500800];

					FILE* file0;
					fopen_s(&file0, "Tables\\co_cp1.bin", "rb");
					fread(co_cp_prune_table_E, 1, 44089920, file0);
					fclose(file0);

					FILE* file4;
					fopen_s(&file4, "Tables\\cp_mep1.bin", "rb");
					fread(cp_mep_prune_table_E, 1, 239500800, file4);
					fclose(file4);

					FILE* file5;
					fopen_s(&file5, "Tables\\cp_eep1.bin", "rb");
					fread(cp_eep_prune_table_E, 1, 239500800, file5);
					fclose(file5);

					FILE* file6;
					fopen_s(&file6, "Tables\\cp_sep1.bin", "rb");
					fread(cp_sep_prune_table_E, 1, 239500800, file6);
					fclose(file6);

					if (forbidden == 0) {
						x_rotation_move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'", "R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" };
						for (int i = 47; i < 53; ++i) {
							if (std::stoi(argv[i]) == 1) {
								move_name_index_E.emplace_back(3 * i - 141);
								move_name_index_E.emplace_back(3 * i - 139);
							}
						}
					}

					else if (forbidden == 15) {
						x_rotation_move_names = { "B", "B2", "B'", "F", "F2", "F'", "L", "L2", "L'", "R", "R2", "R'", "U", "U2", "U'", "D", "D2", "D'" };
						for (int i = 47; i < 53; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[4][0], gen[4][2] });
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[5][0], gen[5][2] });
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[2][0], gen[2][2] });
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[3][0], gen[3][2] });
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[1][0], gen[1][2] });
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[0][0], gen[0][2] });
								}
							}
						}
					}

					else if (forbidden == 12) {
						x_rotation_move_names = { "F", "F2", "F'", "B", "B2", "B'", "L", "L2", "L'", "R", "R2", "R'", "D", "D2", "D'", "U", "U2", "U'" };
						for (int i = 47; i < 53; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[5][0], gen[5][2] });
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[4][0], gen[4][2] });
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[2][0], gen[2][2] });
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[3][0], gen[3][2] });
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[1][0], gen[1][2] });
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[1][0], gen[1][2] });
								}
							}
						}
					}

					Search_PLL1 solution(scrambled_state);

					solution.start_search(min_length, max_length, sol_num);
				}
			}

			else {

				center_move_table_E.reserve(24);

				const Value& center_move_tbl = doc1["CENTER_MOVE_TABLE"].GetArray();
				for (auto& d : center_move_tbl.GetArray()) {
					//const auto e = d.GetArray();
					std::vector<int> X;
					X.reserve(45);
					for (auto& f : d.GetArray()) {
						//int i = 0;
						const int g = f.GetInt();
						X.emplace_back(g);
						//++i;
					}
					center_move_table_E.emplace_back(X);
				}

				std::vector<int> Cpp_cp;
				std::vector<int> Cpp_co;
				std::vector<int> Cpp_ep;
				std::vector<int> Cpp_eo;
				std::vector<int> Cpp_center;
				Cpp_cp.reserve(8);
				Cpp_co.reserve(8);
				Cpp_ep.reserve(12);
				Cpp_eo.reserve(12);
				Cpp_center.reserve(6);

				std::vector<std::vector<int>> gen = { { 0, 1, 2 }, { 3, 4, 5 }, { 6, 7, 8 }, { 9, 10, 11 }, { 12, 13, 14 }, { 15, 16, 17 }, { 18, 19, 20 }, { 21, 22, 23 }, { 24, 25, 26 }, { 27, 28, 29 }, { 30, 31, 32 }, { 33, 34, 35 }, { 36, 37, 38 }, { 39, 40, 41 }, { 42, 43, 44 } };

				for (int i = 1; i < 9; ++i) {
					Cpp_cp.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 9; i < 17; ++i) {
					Cpp_co.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 17; i < 29; ++i) {
					Cpp_ep.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 29; i < 41; ++i) {
					Cpp_eo.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 41; i < 47; ++i) {
					Cpp_center.emplace_back(std::stoi(argv[i]));
				}

				int min_length = std::stoi(argv[62]);
				int max_length = std::stoi(argv[63]);
				int sol_num = std::stoi(argv[64]);

				State_fs scrambled_state(Cpp_cp, Cpp_co, Cpp_ep, Cpp_eo, Cpp_center);

				if (std::stoi(argv[65]) == 2) {

					co_cp_prune_table_E = new unsigned char[44089920];
					cp_mep_prune_table_E = new unsigned char[239500800];
					co_eo_center_prune_table_E = new unsigned char[53747712];

					FILE* file0;
					fopen_s(&file0, "Tables\\co_cp2.bin", "rb");
					fread(co_cp_prune_table_E, 1, 44089920, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, "Tables\\cp_mep2.bin", "rb");
					fread(cp_mep_prune_table_E, 1, 44089920, file1);
					fclose(file1);

					FILE* file4;
					fopen_s(&file4, "Tables\\co_eo_center2.bin", "rb");
					fread(co_eo_center_prune_table_E, 1, 53747712, file4);
					fclose(file4);

					if (forbidden == 0) {
						x_rotation_move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'", "R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'", "Uw", "Uw2", "Uw'", "Dw", "Dw2", "Dw'", "Lw", "Lw2", "Lw'", "Rw", "Rw2", "Rw'", "Fw", "Fw2", "Fw'", "Bw", "Bw2", "Bw'", "M", "M2", "M'", "E", "E2", "E'", "S", "S2", "S'" };
						for (int i = 47; i < 62; ++i) {
							if (std::stoi(argv[i]) == 1) {
								move_name_index_E.emplace_back(3 * i - 141);
								move_name_index_E.emplace_back(3 * i - 140);
								move_name_index_E.emplace_back(3 * i - 139);
							}
						}
					}

					else if (forbidden == 15) {
						x_rotation_move_names = { "B", "B2", "B'", "F", "F2", "F'", "L", "L2", "L'", "R", "R2", "R'", "U", "U2", "U'", "D", "D2", "D'", "Bw", "Bw2", "Bw'", "Fw", "Fw2", "Fw'", "Lw", "Lw2", "Lw'", "Rw", "Rw2", "Rw'", "Uw", "Uw2", "Uw'", "Dw", "Dw2", "Dw'", "M", "M2", "M'", "S", "S2", "S'", "E", "E2", "E'" };
						for (int i = 47; i < 62; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), gen[4].begin(), gen[4].end());
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), gen[5].begin(), gen[5].end());
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), gen[2].begin(), gen[2].end());
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), gen[3].begin(), gen[3].end());
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), gen[1].begin(), gen[1].end());
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), gen[0].begin(), gen[0].end());
								}
								else if (i == 53) {
									move_name_index_E.insert(move_name_index_E.end(), gen[10].begin(), gen[10].end());
								}
								else if (i == 54) {
									move_name_index_E.insert(move_name_index_E.end(), gen[11].begin(), gen[11].end());
								}
								else if (i == 55) {
									move_name_index_E.insert(move_name_index_E.end(), gen[8].begin(), gen[8].end());
								}
								else if (i == 56) {
									move_name_index_E.insert(move_name_index_E.end(), gen[9].begin(), gen[9].end());
								}
								else if (i == 57) {
									move_name_index_E.insert(move_name_index_E.end(), gen[7].begin(), gen[7].end());
								}
								else if (i == 58) {
									move_name_index_E.insert(move_name_index_E.end(), gen[6].begin(), gen[6].end());
								}
								else if (i == 59) {
									move_name_index_E.insert(move_name_index_E.end(), gen[12].begin(), gen[12].end());
								}
								else if (i == 60) {
									move_name_index_E.insert(move_name_index_E.end(), gen[14].begin(), gen[14].end());
								}
								else if (i == 61) {
									move_name_index_E.insert(move_name_index_E.end(), gen[13].begin(), gen[13].end());
								}
							}
						}
					}

					else if (forbidden == 12) {
						x_rotation_move_names = { "F", "F2", "F'", "B", "B2", "B'", "L", "L2", "L'", "R", "R2", "R'", "D", "D2", "D'", "U", "U2", "U'", "Fw", "Fw2", "Fw'", "Bw", "Bw2", "Bw'", "Lw", "Lw2", "Lw'", "Rw", "Rw2", "Rw'", "Dw", "Dw2", "Dw'", "Uw", "Uw2", "Uw'", "M", "M2", "M'", "S", "S2", "S'", "E", "E2", "E'" };
						for (int i = 47; i < 62; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), gen[5].begin(), gen[5].end());
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), gen[4].begin(), gen[4].end());
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), gen[2].begin(), gen[2].end());
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), gen[3].begin(), gen[3].end());
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), gen[0].begin(), gen[0].end());
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), gen[1].begin(), gen[1].end());
								}
								else if (i == 53) {
									move_name_index_E.insert(move_name_index_E.end(), gen[11].begin(), gen[11].end());
								}
								else if (i == 54) {
									move_name_index_E.insert(move_name_index_E.end(), gen[10].begin(), gen[10].end());
								}
								else if (i == 55) {
									move_name_index_E.insert(move_name_index_E.end(), gen[8].begin(), gen[8].end());
								}
								else if (i == 56) {
									move_name_index_E.insert(move_name_index_E.end(), gen[9].begin(), gen[9].end());
								}
								else if (i == 57) {
									move_name_index_E.insert(move_name_index_E.end(), gen[6].begin(), gen[6].end());
								}
								else if (i == 58) {
									move_name_index_E.insert(move_name_index_E.end(), gen[7].begin(), gen[7].end());
								}
								else if (i == 59) {
									move_name_index_E.insert(move_name_index_E.end(), gen[12].begin(), gen[12].end());
								}
								else if (i == 60) {
									move_name_index_E.insert(move_name_index_E.end(), gen[14].begin(), gen[14].end());
								}
								else if (i == 61) {
									move_name_index_E.insert(move_name_index_E.end(), gen[13].begin(), gen[13].end());
								}
							}
						}
					}

					Search_PLL2 solution(scrambled_state);

					solution.start_search_fs(min_length, max_length, sol_num);
				}

				else if (std::stoi(argv[65]) == 3) {

					co_cp_prune_table_E = new unsigned char[44089920];
					co_eo_center_prune_table_E = new unsigned char[53747712];

					FILE* file0;
					fopen_s(&file0, "Tables\\co_cp3.bin", "rb");
					fread(co_cp_prune_table_E, 1, 44089920, file0);
					fclose(file0);

					FILE* file4;
					fopen_s(&file4, "Tables\\co_eo_center3.bin", "rb");
					fread(co_eo_center_prune_table_E, 1, 53747712, file4);
					fclose(file4);

					if (forbidden == 0) {
						x_rotation_move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'", "R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'", "Uw", "Uw2", "Uw'", "Dw", "Dw2", "Dw'", "Lw", "Lw2", "Lw'", "Rw", "Rw2", "Rw'", "Fw", "Fw2", "Fw'", "Bw", "Bw2", "Bw'", "M", "M2", "M'", "E", "E2", "E'", "S", "S2", "S'" };
						for (int i = 47; i < 62; ++i) {
							if (std::stoi(argv[i]) == 1) {
								move_name_index_E.emplace_back(3 * i - 141);
								move_name_index_E.emplace_back(3 * i - 139);
							}
						}
					}

					else if (forbidden == 15) {
						x_rotation_move_names = { "B", "B2", "B'", "F", "F2", "F'", "L", "L2", "L'", "R", "R2", "R'", "U", "U2", "U'", "D", "D2", "D'", "Bw", "Bw2", "Bw'", "Fw", "Fw2", "Fw'", "Lw", "Lw2", "Lw'", "Rw", "Rw2", "Rw'", "Uw", "Uw2", "Uw'", "Dw", "Dw2", "Dw'", "M", "M2", "M'", "S", "S2", "S'", "E", "E2", "E'" };
						for (int i = 47; i < 62; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[4][0], gen[4][2] });
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[5][0], gen[5][2] });
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[2][0], gen[2][2] });
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[3][0], gen[3][2] });
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[1][0], gen[1][2] });
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[0][0], gen[0][2] });
								}
								else if (i == 53) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[10][0], gen[10][2] });
								}
								else if (i == 54) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[11][0], gen[11][2] });
								}
								else if (i == 55) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[8][0], gen[8][2] });
								}
								else if (i == 56) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[9][0], gen[9][2] });
								}
								else if (i == 57) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[7][0], gen[7][2] });
								}
								else if (i == 58) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[6][0], gen[6][2] });
								}
								else if (i == 59) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[12][0], gen[12][2] });
								}
								else if (i == 60) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[14][0], gen[14][2] });
								}
								else if (i == 61) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[13][0], gen[13][2] });
								}
							}
						}
					}

					else if (forbidden == 12) {
						x_rotation_move_names = { "F", "F2", "F'", "B", "B2", "B'", "L", "L2", "L'", "R", "R2", "R'", "D", "D2", "D'", "U", "U2", "U'", "Fw", "Fw2", "Fw'", "Bw", "Bw2", "Bw'", "Lw", "Lw2", "Lw'", "Rw", "Rw2", "Rw'", "Dw", "Dw2", "Dw'", "Uw", "Uw2", "Uw'", "M", "M2", "M'", "S", "S2", "S'", "E", "E2", "E'" };
						for (int i = 47; i < 62; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[5][0], gen[5][2] });
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[4][0], gen[4][2] });
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[2][0], gen[2][2] });
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[3][0], gen[3][2] });
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[0][0], gen[0][2] });
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[1][0], gen[1][2] });
								}
								else if (i == 53) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[11][0], gen[11][2] });
								}
								else if (i == 54) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[10][0], gen[10][2] });
								}
								else if (i == 55) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[8][0], gen[8][2] });
								}
								else if (i == 56) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[9][0], gen[9][2] });
								}
								else if (i == 57) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[6][0], gen[6][2] });
								}
								else if (i == 58) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[7][0], gen[7][2] });
								}
								else if (i == 59) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[12][0], gen[12][2] });
								}
								else if (i == 60) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[14][0], gen[14][2] });
								}
								else if (i == 61) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[13][0], gen[13][2] });
								}
							}
						}
					}

					Search_PLL3 solution(scrambled_state);

					solution.start_search_fs(min_length, max_length, sol_num);
				}
			}
		}

		else if (pattern == 1) {
			co_move_table_E.reserve(2187);

			const Value& co_move_tbl = doc1["CO_MOVE_TABLE"].GetArray();
			for (auto& d : co_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				co_move_table_E.emplace_back(X);
			}

			cp_move_table_E.reserve(40320);

			const Value& cp_move_tbl = doc1["CP_MOVE_TABLE"].GetArray();
			for (auto& d : cp_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				cp_move_table_E.emplace_back(X);
			}

			if (std::stoi(argv[65]) == 0 || std::stoi(argv[65]) == 1) {

				std::vector<int> Cpp_cp;
				std::vector<int> Cpp_co;
				std::vector<int> Cpp_ep;
				std::vector<int> Cpp_eo;
				Cpp_cp.reserve(8);
				Cpp_co.reserve(8);
				Cpp_ep.reserve(12);
				Cpp_eo.reserve(12);

				std::vector<std::vector<int>> gen = { { 0, 1, 2 }, { 3, 4, 5 }, { 6, 7, 8 }, { 9, 10, 11 }, { 12, 13, 14 }, { 15, 16, 17 } };

				for (int i = 1; i < 9; ++i) {
					Cpp_cp.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 9; i < 17; ++i) {
					Cpp_co.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 17; i < 29; ++i) {
					Cpp_ep.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 29; i < 41; ++i) {
					Cpp_eo.emplace_back(std::stoi(argv[i]));
				}

				int min_length = std::stoi(argv[62]);
				int max_length = std::stoi(argv[63]);
				int sol_num = std::stoi(argv[64]);

				State scrambled_state(Cpp_cp, Cpp_co, Cpp_ep, Cpp_eo);

				if (std::stoi(argv[65]) == 0) {

					co_cp_prune_table_E = new unsigned char[44089920];

					FILE* file0;
					fopen_s(&file0, "Tables\\co_cp0.bin", "rb");
					fread(co_cp_prune_table_E, 1, 44089920, file0);
					fclose(file0);

					if (forbidden == 0) {
						x_rotation_move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'", "R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" };
						for (int i = 47; i < 53; ++i) {
							if (std::stoi(argv[i]) == 1) {
								move_name_index_E.emplace_back(3 * i - 141);
								move_name_index_E.emplace_back(3 * i - 140);
								move_name_index_E.emplace_back(3 * i - 139);
							}
						}
					}

					else if (forbidden == 15) {
						x_rotation_move_names = { "B", "B2", "B'", "F", "F2", "F'", "L", "L2", "L'", "R", "R2", "R'", "U", "U2", "U'", "D", "D2", "D'" };
						for (int i = 47; i < 53; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), gen[4].begin(), gen[4].end());
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), gen[5].begin(), gen[5].end());
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), gen[2].begin(), gen[2].end());
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), gen[3].begin(), gen[3].end());
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), gen[1].begin(), gen[1].end());
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), gen[0].begin(), gen[0].end());
								}
							}
						}
					}

					else if (forbidden == 12) {
						x_rotation_move_names = { "F", "F2", "F'", "B", "B2", "B'", "L", "L2", "L'", "R", "R2", "R'", "D", "D2", "D'", "U", "U2", "U'" };
						for (int i = 47; i < 53; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), gen[5].begin(), gen[5].end());
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), gen[4].begin(), gen[4].end());
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), gen[2].begin(), gen[2].end());
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), gen[3].begin(), gen[3].end());
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), gen[0].begin(), gen[0].end());
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), gen[1].begin(), gen[1].end());
								}
							}
						}
					}

					Search_COLL0 solution(scrambled_state);

					solution.start_search(min_length, max_length, sol_num);
				}

				else if (std::stoi(argv[65]) == 1) {

					co_cp_prune_table_E = new unsigned char[44089920];
					cp_eep_prune_table_E = new unsigned char[239500800];
					eo_cp_prune_table_E = new unsigned char[41287680];
					co_eep_prune_table_E = new unsigned char[12990780];

					FILE* file0;
					fopen_s(&file0, "Tables\\co_cp1.bin", "rb");
					fread(co_cp_prune_table_E, 1, 44089920, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, "Tables\\eo_cp1.bin", "rb");
					fread(eo_cp_prune_table_E, 1, 41287680, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, "Tables\\cp_eep1.bin", "rb");
					fread(cp_eep_prune_table_E, 1, 239500800, file2);
					fclose(file2);

					FILE* file3;
					fopen_s(&file3, "Tables\\co_eep1.bin", "rb");
					fread(co_eep_prune_table_E, 1, 12990780, file3);
					fclose(file3);

					if (forbidden == 0) {
						x_rotation_move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'", "R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" };
						for (int i = 47; i < 53; ++i) {
							if (std::stoi(argv[i]) == 1) {
								move_name_index_E.emplace_back(3 * i - 141);
								move_name_index_E.emplace_back(3 * i - 139);
							}
						}
					}

					else if (forbidden == 15) {
						x_rotation_move_names = { "B", "B2", "B'", "F", "F2", "F'", "L", "L2", "L'", "R", "R2", "R'", "U", "U2", "U'", "D", "D2", "D'" };
						for (int i = 47; i < 53; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[4][0], gen[4][2] });
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[5][0], gen[5][2] });
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[2][0], gen[2][2] });
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[3][0], gen[3][2] });
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[1][0], gen[1][2] });
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[0][0], gen[0][2] });
								}
							}
						}
					}

					else if (forbidden == 12) {
						x_rotation_move_names = { "F", "F2", "F'", "B", "B2", "B'", "L", "L2", "L'", "R", "R2", "R'", "D", "D2", "D'", "U", "U2", "U'" };
						for (int i = 47; i < 53; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[5][0], gen[5][2] });
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[4][0], gen[4][2] });
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[2][0], gen[2][2] });
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[3][0], gen[3][2] });
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[1][0], gen[1][2] });
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[1][0], gen[1][2] });
								}
							}
						}
					}

					Search_COLL1 solution(scrambled_state);

					solution.start_search(min_length, max_length, sol_num);
				}
			}

			else {

				center_move_table_E.reserve(24);

				const Value& center_move_tbl = doc1["CENTER_MOVE_TABLE"].GetArray();
				for (auto& d : center_move_tbl.GetArray()) {
					//const auto e = d.GetArray();
					std::vector<int> X;
					X.reserve(45);
					for (auto& f : d.GetArray()) {
						//int i = 0;
						const int g = f.GetInt();
						X.emplace_back(g);
						//++i;
					}
					center_move_table_E.emplace_back(X);
				}

				std::vector<int> Cpp_cp;
				std::vector<int> Cpp_co;
				std::vector<int> Cpp_ep;
				std::vector<int> Cpp_eo;
				std::vector<int> Cpp_center;
				Cpp_cp.reserve(8);
				Cpp_co.reserve(8);
				Cpp_ep.reserve(12);
				Cpp_eo.reserve(12);
				Cpp_center.reserve(6);

				std::vector<std::vector<int>> gen = { { 0, 1, 2 }, { 3, 4, 5 }, { 6, 7, 8 }, { 9, 10, 11 }, { 12, 13, 14 }, { 15, 16, 17 }, { 18, 19, 20 }, { 21, 22, 23 }, { 24, 25, 26 }, { 27, 28, 29 }, { 30, 31, 32 }, { 33, 34, 35 }, { 36, 37, 38 }, { 39, 40, 41 }, { 42, 43, 44 } };

				for (int i = 1; i < 9; ++i) {
					Cpp_cp.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 9; i < 17; ++i) {
					Cpp_co.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 17; i < 29; ++i) {
					Cpp_ep.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 29; i < 41; ++i) {
					Cpp_eo.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 41; i < 47; ++i) {
					Cpp_center.emplace_back(std::stoi(argv[i]));
				}

				int min_length = std::stoi(argv[62]);
				int max_length = std::stoi(argv[63]);
				int sol_num = std::stoi(argv[64]);

				State_fs scrambled_state(Cpp_cp, Cpp_co, Cpp_ep, Cpp_eo, Cpp_center);

				if (std::stoi(argv[65]) == 2) {

					co_cp_prune_table_E = new unsigned char[44089920];
					co_eo_center_prune_table_E = new unsigned char[53747712];
					co_eep_prune_table_E = new unsigned char[12990780];

					FILE* file0;
					fopen_s(&file0, "Tables\\co_cp2.bin", "rb");
					fread(co_cp_prune_table_E, 1, 44089920, file0);
					fclose(file0);

					FILE* file2;
					fopen_s(&file2, "Tables\\co_eo_center2.bin", "rb");
					fread(co_eo_center_prune_table_E, 1, 53747712, file2);
					fclose(file2);

					FILE* file3;
					fopen_s(&file3, "Tables\\OLL_co_eep2.bin", "rb");
					fread(co_eep_prune_table_E, 1, 12990780, file3);
					fclose(file3);

					if (forbidden == 0) {
						x_rotation_move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'", "R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'", "Uw", "Uw2", "Uw'", "Dw", "Dw2", "Dw'", "Lw", "Lw2", "Lw'", "Rw", "Rw2", "Rw'", "Fw", "Fw2", "Fw'", "Bw", "Bw2", "Bw'", "M", "M2", "M'", "E", "E2", "E'", "S", "S2", "S'" };
						for (int i = 47; i < 62; ++i) {
							if (std::stoi(argv[i]) == 1) {
								move_name_index_E.emplace_back(3 * i - 141);
								move_name_index_E.emplace_back(3 * i - 140);
								move_name_index_E.emplace_back(3 * i - 139);
							}
						}
					}

					else if (forbidden == 15) {
						x_rotation_move_names = { "B", "B2", "B'", "F", "F2", "F'", "L", "L2", "L'", "R", "R2", "R'", "U", "U2", "U'", "D", "D2", "D'", "Bw", "Bw2", "Bw'", "Fw", "Fw2", "Fw'", "Lw", "Lw2", "Lw'", "Rw", "Rw2", "Rw'", "Uw", "Uw2", "Uw'", "Dw", "Dw2", "Dw'", "M", "M2", "M'", "S", "S2", "S'", "E", "E2", "E'" };
						for (int i = 47; i < 62; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), gen[4].begin(), gen[4].end());
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), gen[5].begin(), gen[5].end());
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), gen[2].begin(), gen[2].end());
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), gen[3].begin(), gen[3].end());
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), gen[1].begin(), gen[1].end());
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), gen[0].begin(), gen[0].end());
								}
								else if (i == 53) {
									move_name_index_E.insert(move_name_index_E.end(), gen[10].begin(), gen[10].end());
								}
								else if (i == 54) {
									move_name_index_E.insert(move_name_index_E.end(), gen[11].begin(), gen[11].end());
								}
								else if (i == 55) {
									move_name_index_E.insert(move_name_index_E.end(), gen[8].begin(), gen[8].end());
								}
								else if (i == 56) {
									move_name_index_E.insert(move_name_index_E.end(), gen[9].begin(), gen[9].end());
								}
								else if (i == 57) {
									move_name_index_E.insert(move_name_index_E.end(), gen[7].begin(), gen[7].end());
								}
								else if (i == 58) {
									move_name_index_E.insert(move_name_index_E.end(), gen[6].begin(), gen[6].end());
								}
								else if (i == 59) {
									move_name_index_E.insert(move_name_index_E.end(), gen[12].begin(), gen[12].end());
								}
								else if (i == 60) {
									move_name_index_E.insert(move_name_index_E.end(), gen[14].begin(), gen[14].end());
								}
								else if (i == 61) {
									move_name_index_E.insert(move_name_index_E.end(), gen[13].begin(), gen[13].end());
								}
							}
						}
					}

					else if (forbidden == 12) {
						x_rotation_move_names = { "F", "F2", "F'", "B", "B2", "B'", "L", "L2", "L'", "R", "R2", "R'", "D", "D2", "D'", "U", "U2", "U'", "Fw", "Fw2", "Fw'", "Bw", "Bw2", "Bw'", "Lw", "Lw2", "Lw'", "Rw", "Rw2", "Rw'", "Dw", "Dw2", "Dw'", "Uw", "Uw2", "Uw'", "M", "M2", "M'", "S", "S2", "S'", "E", "E2", "E'" };
						for (int i = 47; i < 62; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), gen[5].begin(), gen[5].end());
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), gen[4].begin(), gen[4].end());
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), gen[2].begin(), gen[2].end());
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), gen[3].begin(), gen[3].end());
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), gen[0].begin(), gen[0].end());
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), gen[1].begin(), gen[1].end());
								}
								else if (i == 53) {
									move_name_index_E.insert(move_name_index_E.end(), gen[11].begin(), gen[11].end());
								}
								else if (i == 54) {
									move_name_index_E.insert(move_name_index_E.end(), gen[10].begin(), gen[10].end());
								}
								else if (i == 55) {
									move_name_index_E.insert(move_name_index_E.end(), gen[8].begin(), gen[8].end());
								}
								else if (i == 56) {
									move_name_index_E.insert(move_name_index_E.end(), gen[9].begin(), gen[9].end());
								}
								else if (i == 57) {
									move_name_index_E.insert(move_name_index_E.end(), gen[6].begin(), gen[6].end());
								}
								else if (i == 58) {
									move_name_index_E.insert(move_name_index_E.end(), gen[7].begin(), gen[7].end());
								}
								else if (i == 59) {
									move_name_index_E.insert(move_name_index_E.end(), gen[12].begin(), gen[12].end());
								}
								else if (i == 60) {
									move_name_index_E.insert(move_name_index_E.end(), gen[14].begin(), gen[14].end());
								}
								else if (i == 61) {
									move_name_index_E.insert(move_name_index_E.end(), gen[13].begin(), gen[13].end());
								}
							}
						}
					}

					Search_COLL2 solution(scrambled_state);

					solution.start_search_fs(min_length, max_length, sol_num);
				}

				else if (std::stoi(argv[65]) == 3) {

					co_cp_prune_table_E = new unsigned char[44089920];
					cp_eep_prune_table_E = new unsigned char[239500800];
					co_eo_center_prune_table_E = new unsigned char[53747712];
					co_eep_prune_table_E = new unsigned char[12990780];

					FILE* file0;
					fopen_s(&file0, "Tables\\co_cp3.bin", "rb");
					fread(co_cp_prune_table_E, 1, 44089920, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, "Tables\\cp_eep3.bin", "rb");
					fread(cp_eep_prune_table_E, 1, 44089920, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, "Tables\\co_eo_center3.bin", "rb");
					fread(co_eo_center_prune_table_E, 1, 53747712, file2);
					fclose(file2);

					FILE* file3;
					fopen_s(&file3, "Tables\\OLL_co_eep3.bin", "rb");
					fread(co_eep_prune_table_E, 1, 12990780, file3);
					fclose(file3);

					if (forbidden == 0) {
						x_rotation_move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'", "R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'", "Uw", "Uw2", "Uw'", "Dw", "Dw2", "Dw'", "Lw", "Lw2", "Lw'", "Rw", "Rw2", "Rw'", "Fw", "Fw2", "Fw'", "Bw", "Bw2", "Bw'", "M", "M2", "M'", "E", "E2", "E'", "S", "S2", "S'" };
						for (int i = 47; i < 62; ++i) {
							if (std::stoi(argv[i]) == 1) {
								move_name_index_E.emplace_back(3 * i - 141);
								move_name_index_E.emplace_back(3 * i - 139);
							}
						}
					}

					else if (forbidden == 15) {
						x_rotation_move_names = { "B", "B2", "B'", "F", "F2", "F'", "L", "L2", "L'", "R", "R2", "R'", "U", "U2", "U'", "D", "D2", "D'", "Bw", "Bw2", "Bw'", "Fw", "Fw2", "Fw'", "Lw", "Lw2", "Lw'", "Rw", "Rw2", "Rw'", "Uw", "Uw2", "Uw'", "Dw", "Dw2", "Dw'", "M", "M2", "M'", "S", "S2", "S'", "E", "E2", "E'" };
						for (int i = 47; i < 62; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[4][0], gen[4][2] });
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[5][0], gen[5][2] });
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[2][0], gen[2][2] });
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[3][0], gen[3][2] });
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[1][0], gen[1][2] });
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[0][0], gen[0][2] });
								}
								else if (i == 53) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[10][0], gen[10][2] });
								}
								else if (i == 54) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[11][0], gen[11][2] });
								}
								else if (i == 55) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[8][0], gen[8][2] });
								}
								else if (i == 56) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[9][0], gen[9][2] });
								}
								else if (i == 57) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[7][0], gen[7][2] });
								}
								else if (i == 58) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[6][0], gen[6][2] });
								}
								else if (i == 59) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[12][0], gen[12][2] });
								}
								else if (i == 60) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[14][0], gen[14][2] });
								}
								else if (i == 61) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[13][0], gen[13][2] });
								}
							}
						}
					}

					else if (forbidden == 12) {
						x_rotation_move_names = { "F", "F2", "F'", "B", "B2", "B'", "L", "L2", "L'", "R", "R2", "R'", "D", "D2", "D'", "U", "U2", "U'", "Fw", "Fw2", "Fw'", "Bw", "Bw2", "Bw'", "Lw", "Lw2", "Lw'", "Rw", "Rw2", "Rw'", "Dw", "Dw2", "Dw'", "Uw", "Uw2", "Uw'", "M", "M2", "M'", "S", "S2", "S'", "E", "E2", "E'" };
						for (int i = 47; i < 62; ++i) {
							if (std::stoi(argv[i]) == 1) {
								if (i == 47) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[5][0], gen[5][2] });
								}
								else if (i == 48) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[4][0], gen[4][2] });
								}
								else if (i == 49) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[2][0], gen[2][2] });
								}
								else if (i == 50) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[3][0], gen[3][2] });
								}
								else if (i == 51) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[0][0], gen[0][2] });
								}
								else if (i == 52) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[1][0], gen[1][2] });
								}
								else if (i == 53) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[11][0], gen[11][2] });
								}
								else if (i == 54) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[10][0], gen[10][2] });
								}
								else if (i == 55) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[8][0], gen[8][2] });
								}
								else if (i == 56) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[9][0], gen[9][2] });
								}
								else if (i == 57) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[6][0], gen[6][2] });
								}
								else if (i == 58) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[7][0], gen[7][2] });
								}
								else if (i == 59) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[12][0], gen[12][2] });
								}
								else if (i == 60) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[14][0], gen[14][2] });
								}
								else if (i == 61) {
									move_name_index_E.insert(move_name_index_E.end(), { gen[13][0], gen[13][2] });
								}
							}
						}
					}

					Search_COLL3 solution(scrambled_state);

					solution.start_search_fs(min_length, max_length, sol_num);
				}
			}
		}

		else if (pattern == 2) {
			std::ifstream ifs2("pre_culculation_F2L.json");
			IStreamWrapper isw2(ifs2);
			Document doc2;
			doc2.ParseStream(isw2);
            pattern = 3;

			co_move_table_E.reserve(5670);

			const Value& co_move_tbl = doc2["F2L_CO3_MOVE_TABLE"].GetArray();
			for (auto& d : co_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				co_move_table_E.emplace_back(X);
			}

			cp_move_table_E.reserve(1680);

			const Value& cp_move_tbl = doc2["F2L_CP3_MOVE_TABLE"].GetArray();
			for (auto& d : cp_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				cp_move_table_E.emplace_back(X);
			}

			if (std::stoi(argv[65]) == 0 || std::stoi(argv[65]) == 1) {

				std::vector<int> Cpp_cp;
				std::vector<int> Cpp_co;
				std::vector<int> Cpp_ep;
				std::vector<int> Cpp_eo;
				Cpp_cp.reserve(8);
				Cpp_co.reserve(8);
				Cpp_ep.reserve(12);
				Cpp_eo.reserve(12);

				for (int i = 1; i < 9; ++i) {
					Cpp_cp.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 9; i < 17; ++i) {
					Cpp_co.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 17; i < 29; ++i) {
					Cpp_ep.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 29; i < 41; ++i) {
					Cpp_eo.emplace_back(std::stoi(argv[i]));
				}

				int min_length = std::stoi(argv[62]);
				int max_length = std::stoi(argv[63]);
				int sol_num = std::stoi(argv[64]);

				State scrambled_state(Cpp_cp, Cpp_co, Cpp_ep, Cpp_eo);

				if (std::stoi(argv[65]) == 0) {

					co_eo_prune_table_E = new unsigned char[5806080];
					co_eep_prune_table_E = new unsigned char[33679800];
					eo_eep_prune_table_E = new unsigned char[12165120];

					FILE* file0;
					fopen_s(&file0, "Tables\\ZBLS_co_eo0.bin", "rb");
					fread(co_eo_prune_table_E, 1, 5806080, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, "Tables\\co_eep-0-3-0.bin", "rb");
					fread(co_eep_prune_table_E, 1, 33679800, file1);
					fclose(file1);

					FILE* file3;
					fopen_s(&file3, "Tables\\OLL_eo_eep0.bin", "rb");
					fread(eo_eep_prune_table_E, 1, 12165120, file3);
					fclose(file3);

					for (int i = 47; i < 53; ++i) {
						if (std::stoi(argv[i]) == 1) {
							move_name_index_E.emplace_back(3 * i - 141);
							move_name_index_E.emplace_back(3 * i - 140);
							move_name_index_E.emplace_back(3 * i - 139);
						}
					}

					Search_ZBLS0 solution(scrambled_state);

					solution.start_search(min_length, max_length, sol_num);
				}

				else if (std::stoi(argv[65]) == 1) {

					co_eo_prune_table_E = new unsigned char[5806080];
					eo_eep_prune_table_E = new unsigned char[12165120];
					co_eep_prune_table_E = new unsigned char[33679800];

					FILE* file0;
					fopen_s(&file0, "Tables\\ZBLS_co_eo1.bin", "rb");
					fread(co_eo_prune_table_E, 1, 5806080, file0);
					fclose(file0);

					FILE* file2;
					fopen_s(&file2, "Tables\\OLL_eo_eep1.bin", "rb");
					fread(eo_eep_prune_table_E, 1, 12165120, file2);
					fclose(file2);

					FILE* file3;
					fopen_s(&file3, "Tables\\co_eep-1-3-0.bin", "rb");
					fread(co_eep_prune_table_E, 1, 33679800, file3);
					fclose(file3);

					for (int i = 47; i < 53; ++i) {
						if (std::stoi(argv[i]) == 1) {
							move_name_index_E.emplace_back(3 * i - 141);
							move_name_index_E.emplace_back(3 * i - 139);
						}
					}

					Search_ZBLS1 solution(scrambled_state);

					solution.start_search(min_length, max_length, sol_num);
				}
			}

			else {

				center_move_table_E.reserve(24);

				const Value& center_move_tbl = doc1["CENTER_MOVE_TABLE"].GetArray();
				for (auto& d : center_move_tbl.GetArray()) {
					//const auto e = d.GetArray();
					std::vector<int> X;
					X.reserve(45);
					for (auto& f : d.GetArray()) {
						//int i = 0;
						const int g = f.GetInt();
						X.emplace_back(g);
						//++i;
					}
					center_move_table_E.emplace_back(X);
				}

				std::vector<int> Cpp_cp;
				std::vector<int> Cpp_co;
				std::vector<int> Cpp_ep;
				std::vector<int> Cpp_eo;
				std::vector<int> Cpp_center;
				Cpp_cp.reserve(8);
				Cpp_co.reserve(8);
				Cpp_ep.reserve(12);
				Cpp_eo.reserve(12);
				Cpp_center.reserve(6);

				std::vector<std::vector<int>> gen = { { 0, 1, 2 }, { 3, 4, 5 }, { 6, 7, 8 }, { 9, 10, 11 }, { 12, 13, 14 }, { 15, 16, 17 }, { 18, 19, 20 }, { 21, 22, 23 }, { 24, 25, 26 }, { 27, 28, 29 }, { 30, 31, 32 }, { 33, 34, 35 }, { 36, 37, 38 }, { 39, 40, 41 }, { 42, 43, 44 } };

				for (int i = 1; i < 9; ++i) {
					Cpp_cp.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 9; i < 17; ++i) {
					Cpp_co.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 17; i < 29; ++i) {
					Cpp_ep.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 29; i < 41; ++i) {
					Cpp_eo.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 41; i < 47; ++i) {
					Cpp_center.emplace_back(std::stoi(argv[i]));
				}

				int min_length = std::stoi(argv[62]);
				int max_length = std::stoi(argv[63]);
				int sol_num = std::stoi(argv[64]);

				State_fs scrambled_state(Cpp_cp, Cpp_co, Cpp_ep, Cpp_eo, Cpp_center);

				if (std::stoi(argv[65]) == 2) {

					eo_eep_prune_table_E = new unsigned char[12165120];
					co_eo_center_prune_table_E = new unsigned char[139345920];
					cp_eep_center_prune_table_E = new unsigned char[239500800];

					FILE* file1;
					fopen_s(&file1, "Tables\\OLL_eo_eep2.bin", "rb");
					fread(eo_eep_prune_table_E, 1, 12165120, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, "Tables\\ZBLS_co_eo_center2.bin", "rb");
					fread(co_eo_center_prune_table_E, 1, 139345920, file2);
					fclose(file2);

					FILE* file3;
					fopen_s(&file3, "Tables\\OLL_cp_eep_center2.bin", "rb");
					fread(cp_eep_center_prune_table_E, 1, 239500800, file3);
					fclose(file3);

					for (int i = 47; i < 62; ++i) {
						if (std::stoi(argv[i]) == 1) {
							move_name_index_E.emplace_back(3 * i - 141);
							move_name_index_E.emplace_back(3 * i - 140);
							move_name_index_E.emplace_back(3 * i - 139);
						}
					}

					Search_ZBLS2 solution(scrambled_state);

					solution.start_search_fs(min_length, max_length, sol_num);
				}

				else if (std::stoi(argv[65]) == 3) {

					co_eo_center_prune_table_E = new unsigned char[139345920];
					cp_eep_center_prune_table_E = new unsigned char[239500800];

					FILE* file2;
					fopen_s(&file2, "Tables\\ZBLS_co_eo_center3.bin", "rb");
					fread(co_eo_center_prune_table_E, 1, 139345920, file2);
					fclose(file2);

					FILE* file3;
					fopen_s(&file3, "Tables\\OLL_cp_eep_center3.bin", "rb");
					fread(cp_eep_center_prune_table_E, 1, 239500800, file3);
					fclose(file3);

					for (int i = 47; i < 62; ++i) {
						if (std::stoi(argv[i]) == 1) {
							move_name_index_E.emplace_back(3 * i - 141);
							move_name_index_E.emplace_back(3 * i - 139);
						}
					}

					Search_ZBLS3 solution(scrambled_state);

					solution.start_search_fs(min_length, max_length, sol_num);
				}
			}
		}

		else if (pattern == 3) {
			co_move_table_E.reserve(2187);

			const Value& co_move_tbl = doc1["CO_MOVE_TABLE"].GetArray();
			for (auto& d : co_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				co_move_table_E.emplace_back(X);
			}

			cp_move_table_E.reserve(1680);

			const Value& OLL_cp_move_tbl = doc1["OLL_CP_MOVE_TABLE"].GetArray();
			for (auto& d : OLL_cp_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				cp_move_table_E.emplace_back(X);
			}

			if (std::stoi(argv[65]) == 0 || std::stoi(argv[65]) == 1) {

				std::vector<int> Cpp_cp;
				std::vector<int> Cpp_co;
				std::vector<int> Cpp_ep;
				std::vector<int> Cpp_eo;
				Cpp_cp.reserve(8);
				Cpp_co.reserve(8);
				Cpp_ep.reserve(12);
				Cpp_eo.reserve(12);


				for (int i = 1; i < 9; ++i) {
					Cpp_cp.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 9; i < 17; ++i) {
					Cpp_co.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 17; i < 29; ++i) {
					Cpp_ep.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 29; i < 41; ++i) {
					Cpp_eo.emplace_back(std::stoi(argv[i]));
				}

				int min_length = std::stoi(argv[62]);
				int max_length = std::stoi(argv[63]);
				int sol_num = std::stoi(argv[64]);

				State scrambled_state(Cpp_cp, Cpp_co, Cpp_ep, Cpp_eo);

				if (std::stoi(argv[65]) == 0) {

					co_cp_prune_table_E = new unsigned char[1837080];
					co_eep_prune_table_E = new unsigned char[12990780];
					co_eo_prune_table_E = new unsigned char[2239488];
					eo_eep_prune_table_E = new unsigned char[12165120];

					FILE* file0;
					fopen_s(&file0, "Tables\\OLL_co_cp0.bin", "rb");
					fread(co_cp_prune_table_E, 1, 1837080, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, "Tables\\OLL_co_eep0.bin", "rb");
					fread(co_eep_prune_table_E, 1, 12990780, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, "Tables\\OLL_co_eo0.bin", "rb");
					fread(co_eo_prune_table_E, 1, 2239488, file2);
					fclose(file2);

					FILE* file5;
					fopen_s(&file5, "Tables\\OLL_eo_eep0.bin", "rb");
					fread(eo_eep_prune_table_E, 1, 12165120, file5);
					fclose(file5);

					x_rotation_move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'", "R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" };
					for (int i = 47; i < 53; ++i) {
						if (std::stoi(argv[i]) == 1) {
							move_name_index_E.emplace_back(3 * i - 141);
							move_name_index_E.emplace_back(3 * i - 140);
							move_name_index_E.emplace_back(3 * i - 139);
						}
					}

					Search_OLL0 solution(scrambled_state);

					solution.start_search(min_length, max_length, sol_num);
				}

				else if (std::stoi(argv[65]) == 1) {

					co_cp_prune_table_E = new unsigned char[1837080];
					co_eep_prune_table_E = new unsigned char[12990780];
					co_eo_prune_table_E = new unsigned char[2239488];
					eo_eep_prune_table_E = new unsigned char[12165120];

					FILE* file0;
					fopen_s(&file0, "Tables\\OLL_co_cp1.bin", "rb");
					fread(co_cp_prune_table_E, 1, 1837080, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, "Tables\\OLL_co_eep1.bin", "rb");
					fread(co_eep_prune_table_E, 1, 12990780, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, "Tables\\OLL_co_eo1.bin", "rb");
					fread(co_eo_prune_table_E, 1, 2239488, file2);
					fclose(file2);

					FILE* file4;
					fopen_s(&file4, "Tables\\OLL_eo_eep1.bin", "rb");
					fread(eo_eep_prune_table_E, 1, 12165120, file4);
					fclose(file4);

					x_rotation_move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'", "R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'" };
					for (int i = 47; i < 53; ++i) {
						if (std::stoi(argv[i]) == 1) {
							move_name_index_E.emplace_back(3 * i - 141);
							move_name_index_E.emplace_back(3 * i - 139);
						}
					}

					Search_OLL1 solution(scrambled_state);

					solution.start_search(min_length, max_length, sol_num);
				}
			}

			else {

				center_move_table_E.reserve(24);

				const Value& center_move_tbl = doc1["CENTER_MOVE_TABLE"].GetArray();
				for (auto& d : center_move_tbl.GetArray()) {
					//const auto e = d.GetArray();
					std::vector<int> X;
					X.reserve(45);
					for (auto& f : d.GetArray()) {
						//int i = 0;
						const int g = f.GetInt();
						X.emplace_back(g);
						//++i;
					}
					center_move_table_E.emplace_back(X);
				}

				std::vector<int> Cpp_cp;
				std::vector<int> Cpp_co;
				std::vector<int> Cpp_ep;
				std::vector<int> Cpp_eo;
				std::vector<int> Cpp_center;
				Cpp_cp.reserve(8);
				Cpp_co.reserve(8);
				Cpp_ep.reserve(12);
				Cpp_eo.reserve(12);
				Cpp_center.reserve(6);

				for (int i = 1; i < 9; ++i) {
					Cpp_cp.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 9; i < 17; ++i) {
					Cpp_co.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 17; i < 29; ++i) {
					Cpp_ep.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 29; i < 41; ++i) {
					Cpp_eo.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 41; i < 47; ++i) {
					Cpp_center.emplace_back(std::stoi(argv[i]));
				}

				int min_length = std::stoi(argv[62]);
				int max_length = std::stoi(argv[63]);
				int sol_num = std::stoi(argv[64]);

				State_fs scrambled_state(Cpp_cp, Cpp_co, Cpp_ep, Cpp_eo, Cpp_center);

				if (std::stoi(argv[65]) == 2) {

					co_cp_prune_table_E = new unsigned char[1837080];
					co_eep_prune_table_E = new unsigned char[12990780];
					eo_eep_prune_table_E = new unsigned char[12165120];
					co_eo_center_prune_table_E = new unsigned char[53747712];
					cp_eep_center_prune_table_E = new unsigned char[239500800];

					FILE* file0;
					fopen_s(&file0, "Tables\\OLL_co_cp2.bin", "rb");
					fread(co_cp_prune_table_E, 1, 1837080, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, "Tables\\OLL_co_eep2.bin", "rb");
					fread(co_eep_prune_table_E, 1, 9979200, file1);
					fclose(file1);

					FILE* file3;
					fopen_s(&file3, "Tables\\OLL_eo_eep2.bin", "rb");
					fread(eo_eep_prune_table_E, 1, 12165120, file3);
					fclose(file3);

					FILE* file4;
					fopen_s(&file4, "Tables\\co_eo_center2.bin", "rb");
					fread(co_eo_center_prune_table_E, 1, 53747712, file4);
					fclose(file4);

					FILE* file5;
					fopen_s(&file5, "Tables\\OLL_cp_eep_center2.bin", "rb");
					fread(cp_eep_center_prune_table_E, 1, 239500800, file5);
					fclose(file5);

					x_rotation_move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'", "R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'", "Uw", "Uw2", "Uw'", "Dw", "Dw2", "Dw'", "Lw", "Lw2", "Lw'", "Rw", "Rw2", "Rw'", "Fw", "Fw2", "Fw'", "Bw", "Bw2", "Bw'", "M", "M2", "M'", "E", "E2", "E'", "S", "S2", "S'" };
					for (int i = 47; i < 62; ++i) {
						if (std::stoi(argv[i]) == 1) {
							move_name_index_E.emplace_back(3 * i - 141);
							move_name_index_E.emplace_back(3 * i - 140);
							move_name_index_E.emplace_back(3 * i - 139);
						}
					}

					Search_OLL2 solution(scrambled_state);

					solution.start_search_fs(min_length, max_length, sol_num);
				}

				else if (std::stoi(argv[65]) == 3) {

					co_cp_prune_table_E = new unsigned char[1837080];
					co_eep_prune_table_E = new unsigned char[12990780];
					cp_eep_prune_table_E = new unsigned char[9979200];
					co_eo_center_prune_table_E = new unsigned char[53747712];

					FILE* file0;
					fopen_s(&file0, "Tables\\OLL_co_cp3.bin", "rb");
					fread(co_cp_prune_table_E, 1, 1837080, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, "Tables\\OLL_co_eep3.bin", "rb");
					fread(co_eep_prune_table_E, 1, 12990780, file1);
					fclose(file1);

					FILE* file3;
					fopen_s(&file3, "Tables\\OLL_cp_eep3.bin", "rb");
					fread(cp_eep_prune_table_E, 1, 9979200, file3);
					fclose(file3);

					FILE* file4;
					fopen_s(&file4, "Tables\\co_eo_center3.bin", "rb");
					fread(co_eo_center_prune_table_E, 1, 53747712, file4);
					fclose(file4);

					x_rotation_move_names = { "U", "U2", "U'", "D", "D2", "D'", "L", "L2", "L'", "R", "R2", "R'", "F", "F2", "F'", "B", "B2", "B'", "Uw", "Uw2", "Uw'", "Dw", "Dw2", "Dw'", "Lw", "Lw2", "Lw'", "Rw", "Rw2", "Rw'", "Fw", "Fw2", "Fw'", "Bw", "Bw2", "Bw'", "M", "M2", "M'", "E", "E2", "E'", "S", "S2", "S'" };
					for (int i = 47; i < 62; ++i) {
						if (std::stoi(argv[i]) == 1) {
							move_name_index_E.emplace_back(3 * i - 141);
							move_name_index_E.emplace_back(3 * i - 139);
						}
					}

					Search_OLL3 solution(scrambled_state);

					solution.start_search_fs(min_length, max_length, sol_num);
				}
			}
		}

		else if (pattern == 4 || pattern == 5) {
			solved_co = solved_index1["co"][14];
			solved_cp = solved_index1["cp"][14];
			solved_eo = solved_index2["eo"][14];
			solved_mep = solved_index2["mep"][14];
			solved_eep = solved_index2["eep"][14];
			solved_sep = solved_index2["sep"][14];

			std::ifstream ifs2("pre_culculation_F2L.json");
			IStreamWrapper isw2(ifs2);
			Document doc2;
			doc2.ParseStream(isw2);

			co_move_table_E.reserve(5670);

			const Value& co_move_tbl = doc2["F2L_CO3_MOVE_TABLE"].GetArray();
			for (auto& d : co_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				co_move_table_E.emplace_back(X);
			}

			cp_move_table_E.reserve(1680);

			const Value& cp_move_tbl = doc2["F2L_CP3_MOVE_TABLE"].GetArray();
			for (auto& d : cp_move_tbl.GetArray()) {
				//const auto e = d.GetArray();
				std::vector<int> X;
				X.reserve(45);
				for (auto& f : d.GetArray()) {
					//int i = 0;
					const int g = f.GetInt();
					X.emplace_back(g);
					//++i;
				}
				cp_move_table_E.emplace_back(X);
			}

			if (std::stoi(argv[65]) == 0 || std::stoi(argv[65]) == 1) {

				std::vector<int> Cpp_cp;
				std::vector<int> Cpp_co;
				std::vector<int> Cpp_ep;
				std::vector<int> Cpp_eo;
				Cpp_cp.reserve(8);
				Cpp_co.reserve(8);
				Cpp_ep.reserve(12);
				Cpp_eo.reserve(12);

				for (int i = 1; i < 9; ++i) {
					Cpp_cp.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 9; i < 17; ++i) {
					Cpp_co.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 17; i < 29; ++i) {
					Cpp_ep.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 29; i < 41; ++i) {
					Cpp_eo.emplace_back(std::stoi(argv[i]));
				}

				int min_length = std::stoi(argv[62]);
				int max_length = std::stoi(argv[63]);
				int sol_num = std::stoi(argv[64]);

				State scrambled_state(Cpp_cp, Cpp_co, Cpp_ep, Cpp_eo);

				if (std::stoi(argv[65]) == 0) {
					co_eep_prune_table_E = new unsigned char[33679800];
					co_sep_prune_table_E = new unsigned char[33679800];
					co_mep_prune_table_E = new unsigned char[33679800];
					eo_eep_prune_table_E = new unsigned char[12165120];
					cp_eep_prune_table_E = new unsigned char[9979200];

					FILE* file0;
					fopen_s(&file0, "Tables\\co_eep-0-3-0.bin", "rb");
					fread(co_eep_prune_table_E, 1, 33679800, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, "Tables\\co_sep-0-3-0.bin", "rb");
					fread(co_sep_prune_table_E, 1, 33679800, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, "Tables\\co_mep-0-3-0.bin", "rb");
					fread(co_mep_prune_table_E, 1, 33679800, file2);
					fclose(file2);

					FILE* file3;
					fopen_s(&file3, "Tables\\eo_eep-0-3-0.bin", "rb");
					fread(eo_eep_prune_table_E, 1, 12165120, file3);
					fclose(file3);

					FILE* file4;
					fopen_s(&file4, "Tables\\cp_eep-0-3-0.bin", "rb");
					fread(cp_eep_prune_table_E, 1, 9979200, file4);
					fclose(file4);

					pattern = 3;

					for (int i = 47; i < 53; ++i) {
						if (std::stoi(argv[i]) == 1) {
							move_name_index_E.emplace_back(3 * i - 141);
							move_name_index_E.emplace_back(3 * i - 140);
							move_name_index_E.emplace_back(3 * i - 139);
						}
					}

					Search_F2L0 solution(scrambled_state);

					solution.start_search(min_length, max_length, sol_num);
				}

				else if (std::stoi(argv[65]) == 1) {
					co_eep_prune_table_E = new unsigned char[33679800];
					co_sep_prune_table_E = new unsigned char[33679800];
					co_mep_prune_table_E = new unsigned char[33679800];
					eo_eep_prune_table_E = new unsigned char[12165120];
					cp_eep_prune_table_E = new unsigned char[9979200];

					FILE* file0;
					fopen_s(&file0, "Tables\\co_eep-1-3-0.bin", "rb");
					fread(co_eep_prune_table_E, 1, 33679800, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, "Tables\\co_sep-1-3-0.bin", "rb");
					fread(co_sep_prune_table_E, 1, 33679800, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, "Tables\\co_mep-1-3-0.bin", "rb");
					fread(co_mep_prune_table_E, 1, 33679800, file2);
					fclose(file2);

					FILE* file3;
					fopen_s(&file3, "Tables\\eo_eep-1-3-0.bin", "rb");
					fread(eo_eep_prune_table_E, 1, 12165120, file3);
					fclose(file3);

					FILE* file4;
					fopen_s(&file4, "Tables\\cp_eep-1-3-0.bin", "rb");
					fread(cp_eep_prune_table_E, 1, 9979200, file4);
					fclose(file4);

					pattern = 3;

					for (int i = 47; i < 53; ++i) {
						if (std::stoi(argv[i]) == 1) {
							move_name_index_E.emplace_back(3 * i - 141);
							move_name_index_E.emplace_back(3 * i - 139);
						}
					}

					Search_F2L1 solution(scrambled_state);

					solution.start_search(min_length, max_length, sol_num);
				}
			}

			else {

				center_move_table_E.reserve(24);

				const Value& center_move_tbl = doc1["CENTER_MOVE_TABLE"].GetArray();
				for (auto& d : center_move_tbl.GetArray()) {
					//const auto e = d.GetArray();
					std::vector<int> X;
					X.reserve(45);
					for (auto& f : d.GetArray()) {
						//int i = 0;
						const int g = f.GetInt();
						X.emplace_back(g);
						//++i;
					}
					center_move_table_E.emplace_back(X);
				}

				std::vector<int> Cpp_cp;
				std::vector<int> Cpp_co;
				std::vector<int> Cpp_ep;
				std::vector<int> Cpp_eo;
				std::vector<int> Cpp_center;
				Cpp_cp.reserve(8);
				Cpp_co.reserve(8);
				Cpp_ep.reserve(12);
				Cpp_eo.reserve(12);
				Cpp_center.reserve(6);

				for (int i = 1; i < 9; ++i) {
					Cpp_cp.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 9; i < 17; ++i) {
					Cpp_co.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 17; i < 29; ++i) {
					Cpp_ep.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 29; i < 41; ++i) {
					Cpp_eo.emplace_back(std::stoi(argv[i]));
				}

				for (int i = 41; i < 47; ++i) {
					Cpp_center.emplace_back(std::stoi(argv[i]));
				}

				int min_length = std::stoi(argv[62]);
				int max_length = std::stoi(argv[63]);
				int sol_num = std::stoi(argv[64]);

				State_fs scrambled_state(Cpp_cp, Cpp_co, Cpp_ep, Cpp_eo, Cpp_center);

				if (std::stoi(argv[65]) == 2) {
					co_eep_prune_table_E = new unsigned char[33679800];
					co_sep_prune_table_E = new unsigned char[33679800];
					co_mep_prune_table_E = new unsigned char[33679800];
					cp_eep_prune_table_E = new unsigned char[9979200];

					FILE* file0;
					fopen_s(&file0, "Tables\\co_eep-2-3-0.bin", "rb");
					fread(co_eep_prune_table_E, 1, 33679800, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, "Tables\\co_sep-2-3-0.bin", "rb");
					fread(co_sep_prune_table_E, 1, 33679800, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, "Tables\\co_mep-2-3-0.bin", "rb");
					fread(co_mep_prune_table_E, 1, 33679800, file2);
					fclose(file2);

					FILE* file3;
					fopen_s(&file3, "Tables\\cp_eep-2-3-0.bin", "rb");
					fread(cp_eep_prune_table_E, 1, 9979200, file3);
					fclose(file3);

					pattern = 3;

					for (int i = 47; i < 62; ++i) {
						if (std::stoi(argv[i]) == 1) {
							move_name_index_E.emplace_back(3 * i - 141);
							move_name_index_E.emplace_back(3 * i - 140);
							move_name_index_E.emplace_back(3 * i - 139);
						}
					}

					Search_F2L2 solution(scrambled_state);

					solution.start_search_fs(min_length, max_length, sol_num);
				}

				else if (std::stoi(argv[65]) == 3) {
					co_eep_prune_table_E = new unsigned char[33679800];
					co_sep_prune_table_E = new unsigned char[33679800];
					co_mep_prune_table_E = new unsigned char[33679800];
					cp_eep_prune_table_E = new unsigned char[9979200];

					FILE* file0;
					fopen_s(&file0, "Tables\\co_eep-3-3-0.bin", "rb");
					fread(co_eep_prune_table_E, 1, 33679800, file0);
					fclose(file0);

					FILE* file1;
					fopen_s(&file1, "Tables\\co_sep-3-3-0.bin", "rb");
					fread(co_sep_prune_table_E, 1, 33679800, file1);
					fclose(file1);

					FILE* file2;
					fopen_s(&file2, "Tables\\co_mep-3-3-0.bin", "rb");
					fread(co_mep_prune_table_E, 1, 33679800, file2);
					fclose(file2);

					FILE* file4;
					fopen_s(&file4, "Tables\\cp_eep-3-3-0.bin", "rb");
					fread(cp_eep_prune_table_E, 1, 9979200, file4);
					fclose(file4);

					pattern = 3;

					for (int i = 47; i < 62; ++i) {
						if (std::stoi(argv[i]) == 1) {
							move_name_index_E.emplace_back(3 * i - 141);
							move_name_index_E.emplace_back(3 * i - 139);
						}
					}

					Search_F2L3 solution(scrambled_state);

					solution.start_search_fs(min_length, max_length, sol_num);
				}
			}
		}
	}

	else {
		std::ifstream ifs("pre_culculation.json");
		IStreamWrapper isw(ifs);
		Document doc;
		doc.ParseStream(isw);

		co_move_table.reserve(2187);

		const Value& co_move_tbl = doc["CO_MOVE_TABLE"].GetArray();
		for (auto& d : co_move_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(18);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			co_move_table.emplace_back(X);
		}

		eo_move_table.reserve(2048);

		const Value& eo_move_tbl = doc["EO_MOVE_TABLE"].GetArray();
		for (auto& d : eo_move_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(18);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			eo_move_table.emplace_back(X);
		}

		e_combination_table.reserve(495);

		const Value& e_combination_tbl = doc["E_COMBINATION_TABLE"].GetArray();
		for (auto& d : e_combination_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(18);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			e_combination_table.emplace_back(X);
		}

		cp_move_table.reserve(40320);

		const Value& cp_move_tbl = doc["CP_MOVE_TABLE"].GetArray();
		for (auto& d : cp_move_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(10);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			cp_move_table.emplace_back(X);
		}

		ud_ep_move_table.reserve(40320);

		const Value& ud_ep_move_tbl = doc["UD_EP_MOVE_TABLE"].GetArray();
		for (auto& d : ud_ep_move_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(10);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			ud_ep_move_table.emplace_back(X);
		}

		e_ep_move_table.reserve(24);

		const Value& e_ep_move_tbl = doc["E_EP_MOVE_TABLE"].GetArray();
		for (auto& d : e_ep_move_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(10);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			e_ep_move_table.emplace_back(X);
		}

		co_eec_prune_table.reserve(2187);

		const Value& co_eec_prune_tbl = doc["CO_EEC_PRUNE_TABLE"].GetArray();
		for (auto& d : co_eec_prune_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(495);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			co_eec_prune_table.emplace_back(X);
		}

		eo_eec_prune_table.reserve(2048);

		const Value& eo_eec_prune_tbl = doc["EO_EEC_PRUNE_TABLE"].GetArray();
		for (auto& d : eo_eec_prune_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(495);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			eo_eec_prune_table.emplace_back(X);
		}

		cp_eep_prune_table.reserve(40320);

		const Value& cp_eep_prune_tbl = doc["CP_EEP_PRUNE_TABLE"].GetArray();
		for (auto& d : cp_eep_prune_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(24);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			cp_eep_prune_table.emplace_back(X);
		}

		udep_eep_prune_table.reserve(40320);

		const Value& udep_eep_prune_tbl = doc["UDEP_EEP_PRUNE_TABLE"].GetArray();
		for (auto& d : udep_eep_prune_tbl.GetArray()) {
			//const auto e = d.GetArray();
			std::vector<int> X;
			X.reserve(24);
			for (auto& f : d.GetArray()) {
				//int i = 0;
				const int g = f.GetInt();
				X.emplace_back(g);
				//++i;
			}
			udep_eep_prune_table.emplace_back(X);
		}

		std::vector<int> Cpp_cp_UD;
		std::vector<int> Cpp_co_UD;
		std::vector<int> Cpp_ep_UD;
		std::vector<int> Cpp_eo_UD;
		std::vector<int> Cpp_cp_RL;
		std::vector<int> Cpp_co_RL;
		std::vector<int> Cpp_ep_RL;
		std::vector<int> Cpp_eo_RL;
		std::vector<int> Cpp_cp_FB;
		std::vector<int> Cpp_co_FB;
		std::vector<int> Cpp_ep_FB;
		std::vector<int> Cpp_eo_FB;
		Cpp_cp_UD.reserve(8);
		Cpp_co_UD.reserve(8);
		Cpp_ep_UD.reserve(12);
		Cpp_eo_UD.reserve(12);
		Cpp_cp_RL.reserve(8);
		Cpp_co_RL.reserve(8);
		Cpp_ep_RL.reserve(12);
		Cpp_eo_RL.reserve(12);
		Cpp_cp_FB.reserve(8);
		Cpp_co_FB.reserve(8);
		Cpp_ep_FB.reserve(12);
		Cpp_eo_FB.reserve(12);

		for (int i = 1; i < 9; ++i) {
			Cpp_cp_UD.emplace_back(std::stoi(argv[i]));
		}

		for (int i = 9; i < 17; ++i) {
			Cpp_co_UD.emplace_back(std::stoi(argv[i]));
		}

		for (int i = 17; i < 29; ++i) {
			Cpp_ep_UD.emplace_back(std::stoi(argv[i]));
		}

		for (int i = 29; i < 41; ++i) {
			Cpp_eo_UD.emplace_back(std::stoi(argv[i]));
		}

		for (int i = 41; i < 49; ++i) {
			Cpp_cp_RL.emplace_back(std::stoi(argv[i]));
		}

		for (int i = 49; i < 57; ++i) {
			Cpp_co_RL.emplace_back(std::stoi(argv[i]));
		}

		for (int i = 57; i < 69; ++i) {
			Cpp_ep_RL.emplace_back(std::stoi(argv[i]));
		}

		for (int i = 69; i < 81; ++i) {
			Cpp_eo_RL.emplace_back(std::stoi(argv[i]));
		}

		for (int i = 81; i < 89; ++i) {
			Cpp_cp_FB.emplace_back(std::stoi(argv[i]));
		}

		for (int i = 89; i < 97; ++i) {
			Cpp_co_FB.emplace_back(std::stoi(argv[i]));
		}

		for (int i = 97; i < 109; ++i) {
			Cpp_ep_FB.emplace_back(std::stoi(argv[i]));
		}

		for (int i = 109; i < 121; ++i) {
			Cpp_eo_FB.emplace_back(std::stoi(argv[i]));
		}

		int min_length = std::stoi(argv[121]);
		int max_length = std::stoi(argv[122]);

		State scrambled_state_UD(Cpp_cp_UD, Cpp_co_UD, Cpp_ep_UD, Cpp_eo_UD);
		State scrambled_state_RL(Cpp_cp_RL, Cpp_co_RL, Cpp_ep_RL, Cpp_eo_RL);
		State scrambled_state_FB(Cpp_cp_FB, Cpp_co_FB, Cpp_ep_FB, Cpp_eo_FB);

		Search_UD solution_UD(scrambled_state_UD);
		Search_RL solution_RL(scrambled_state_RL);
		Search_FB solution_FB(scrambled_state_FB);

		std::thread UD_DR(&Search_UD::start_search1, &solution_UD, min_length, max_length);
		std::thread RL_DR(&Search_RL::start_search1, &solution_RL, min_length, max_length);
		std::thread FB_DR(&Search_FB::start_search1, &solution_FB, min_length, max_length);

		UD_DR.join();
		RL_DR.join();
		FB_DR.join();
	}
}
