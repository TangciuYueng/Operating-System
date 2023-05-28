#ifndef VIRADDRESS_H
#define VIRADDRESS_H

class VirAddress
{
private:
    int pageContentID;
    int pageTableID2;
    int pageTableID3;
    int pageOffsets;
public:
    VirAddress();
    int getpageContentID();
    int getpageTableID2();
    int getpageTableID3();
    int getpageOffsets();
    void modifypageContentID(int tar);
    void modifypageTableID2(int tar);
    void modifypageTableID3(int tar);
    void modifypageOffsets(int tar);
};

#endif // VIRADDRESS_H
