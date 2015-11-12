#ifndef KDoEmployee_H
#define KDoEmployee_H

#include "KDo.h"

#ifndef KDOObjectsH
#include "KDoObjects.h"
#endif

#include <string>
#include <list>
#include <map>

#include <string>
using std::string;
using std::list;
using std::map;

using std::string

class KDoEmployee : public KDataPersistentObject
{
public:
	static const string Field_SystemKey;
	static const string Field_SystemKeyType;

	static const string Field_Id;
	static const string Field_ActiveFlag;
	static const string Field_SomeValue;

public:
	KDoRawMaterial *RawMaterial;
	KDoRawMaterialSize *RawMaterialSize;

public:
	string Id;
	unsigned int ActiveFlag;
	float SomeValue;

public:
	friend class KDoFactory;
	static KDoEmployee* CreateDoObject();
	static KDoEmployee* GetDoObject(string m_SystemKey);
	static list<KDoEmployee*> GetDoObjectsByFilter(map<string, string>& m_Filter);
	static list<KDoEmployee*> GetDoObjectsByFilter(map<string, list<string> >& m_Filter);
	static list<KDoEmployee*> GetDoObjectsByFilter(list< map<string, string> >& m_Filter);
	static list<KDoEmployee*> GetDoObjectsByFilter(map<string, string>& m_Filter, int m_StartIndex, int m_Number, list<string>& m_OrderList, bool m_AscendingFlag);
	static list<KDoEmployee*> GetDoObjectsByFilter(map<string, list<string> >& m_Filter, int m_StartIndex, int m_Number, list<string>& m_OrderList, bool m_AscendingFlag);
	static list<KDoEmployee*> GetDoObjectsByFilter(list< map<string, string> >& m_Filter, int m_StartIndex, int m_Number, list<string>& m_OrderList, bool m_AscendingFlag);
	static list<KDoEmployee*> GetDoObjectsBySql(string m_SqlFilter);
	static int GetDoObjectsCountBySql(string m_SqlFilter);
	static int GetDoObjectsCountByFilter(map<string, string>& m_Filter);
	static int GetDoObjectsCountByFilter(map<string, list<string> >& m_Filter);
	static int GetDoObjectsCountByFilter(list< map<string, string> >& m_Filter);
	static int GetDoObjectsCountByFilter(map<string, string>& m_Filter, set<string>& m_LikeColumns);
	static int GetDoObjectsCountByFilter(map<string, list<string> >& m_Filter, set<string>& m_LikeColumns);
	static int GetDoObjectsCountByFilter(list< map<string, string> >& m_Filter, set<string>& m_LikeColumns);
	static list<KDoEmployee*> GetDoObjectsBySql(string m_SqlFilter, int m_StartIndex, int m_Number, list<string>& m_OrderList, bool m_AscendingFlag);
	static list<KDoEmployee*> GetDoObjectsByFilter(map<string, string>& m_Filter, set<string>& m_LikeColumns);
	static list<KDoEmployee*> GetDoObjectsByFilter(map<string, list<string> >& m_Filter, set<string>& m_LikeColumns);
	static list<KDoEmployee*> GetDoObjectsByFilter(list< map<string, string> >& m_Filter, set<string>& m_LikeColumns);
	static list<KDoEmployee*> GetDoObjectsByFilter(map<string, string>& m_Filter, set<string>& m_LikeColumns, int m_StartIndex, int m_Number, list<string>& m_OrderList, bool m_AscendingFlag);
	static list<KDoEmployee*> GetDoObjectsByFilter(map<string, list<string> >& m_Filter, set<string>& m_LikeColumns, int m_StartIndex, int m_Number, list<string>& m_OrderList, bool m_AscendingFlag);
	static list<KDoEmployee*> GetDoObjectsByFilter(list< map<string, string> >& m_Filter, set<string>& m_LikeColumns, int m_StartIndex, int m_Number, list<string>& m_OrderList, bool m_AscendingFlag);
	static KDoEmployee* GetDoObjectByFilter(map<string, string>& m_Filter);
	static KDoEmployee* GetDoObjectBySql(string m_SqlFilter);

public:
	KDoEmployee();

};

#endif