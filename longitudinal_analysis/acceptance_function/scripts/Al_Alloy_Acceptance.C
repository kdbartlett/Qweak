//=============================================================================
// Al_Alloy_Acceptance.C
// Kurtis Bartlett
// 2017/6/27
//
// Script for extracting acceptance e(th, phi, nu)  from 1d and 2d histograms.
// Output sent to .csv for later plotting with Python's matplotlib.pyplot.
//
// Usage:
//  -Environment Variable Setup
//setenv LD_LIBRARY_PATH /u/home/kbartlet/Qweak/QwGeant4/build/:${LD_LIBRARY_PATH}
//  -Compile
//      > ./Al_Alloy_Acceptance_compile.sh
//  -Run
//      > ./Al_Alloy_Acceptance
//=============================================================================

//*****************************************************************************
// Include
//*****************************************************************************

// C/C++ Related
#include <iostream>
#include <fstream>

// ROOT Related
#include "TROOT.h"
#include </u/home/kbartlet/Qweak/QwGeant4/include/QweakSimUserMainEvent.hh>
#include <TChain.h>
#include <TCanvas.h>
#include <TString.h>
#include <TStyle.h>
#include <TAxis.h>
#include <TLatex.h>
#include <TH1D.h>
#include <TH2D.h>
#include <TMath.h>
#include <TAttLine.h>

using namespace std;

TChain * Load_Files(const Char_t *sub_path,
                    Int_t fstart_num,
                    Int_t fend_num,
                    Int_t &fnum)
{
    // Load .root files for analysis
    const Char_t * cache_path = "/cache/home/kbartlet/rootfiles";
    TChain * tree = new TChain("QweakSimG4_Tree");
    Int_t fstatus = 0.0;
    fnum = 0;
    for(Int_t nfile = fstart_num ; nfile < fend_num + 1; nfile++)
    {
        fstatus = tree->AddFile(Form("%s/%s/%s_%d.root",
                                cache_path,
                                sub_path,
                                sub_path,
                                nfile));
        fnum = fnum + fstatus;//Increase fnum with each file chained
    } // End file for loop
    std::cout << "Loading files from: " << Form("/%s/%s/%s_*.root",
                                                cache_path,
                                                sub_path,
                                                sub_path) << endl;
    return tree;
}

void Loop_Tree(TChain *tree,
               TH1D *theta_hist,
               TH1D *phi_hist,
               TH1D *nu_hist,
               TH1D *theta_cut_hist,
               TH1D *phi_cut_hist,
               TH1D *nu_cut_hist,
               TH2D *theta_phi_hist,
               TH2D *theta_nu_hist,
               TH2D *phi_nu_hist,
               TH2D *theta_phi_cut_hist,
               TH2D *theta_nu_cut_hist,
               TH2D *phi_nu_cut_hist)
{
    // Loop over the tree and fill histograms
    
    // Initialize Qweak specific tree variables
    QweakSimUserMainEvent *evt = 0;
    QweakSimUserPrimaryEvent *primary = 0;
    QweakSimUserCerenkov_PMTEvent *pmt = 0;
    QweakSimUserCerenkov_DetectorEvent *detector = 0;
    // Set the appropriate branch address
    tree->SetBranchAddress("QweakSimUserMainEvent", &evt);

    // Get total # of entries in the TChain tree
    Int_t num_entries = tree->GetEntries();

    // Loop over the entries in the tree
    for(Int_t entry = 0; entry < num_entries; entry++)
    {
        //Print status of loop
        if((entry%1000)==0)
        {
            cout << "Processing: " << entry << "/" << num_entries << endl;
        } // End of if print status
    
    // Retrieve an entry from tree
    tree->GetEntry(entry);
        
        // Point to proper branch names
        primary = &(evt->Primary);
        pmt = &(evt->Cerenkov.PMT);
        detector = &(evt->Cerenkov.Detector);

        // Fill uncut histograms
        theta_hist->Fill(TMath::Cos(primary->GetOriginVertexThetaAngle()*(TMath::Pi()/180.0)));
        phi_hist->Fill(primary->GetOriginVertexPhiAngle());
        nu_hist->Fill(primary->GetBeamEnergy() - 
                      primary->GetOriginVertexKineticEnergy());
        theta_phi_hist->Fill(TMath::Cos(primary->GetOriginVertexThetaAngle()*(TMath::Pi()/180.0)), primary->GetOriginVertexPhiAngle());
        theta_nu_hist->Fill(TMath::Cos(primary->GetOriginVertexThetaAngle()*(TMath::Pi()/180.0)), primary->GetBeamEnergy() - primary->GetOriginVertexKineticEnergy());
        phi_nu_hist->Fill(primary->GetOriginVertexPhiAngle(), primary->GetBeamEnergy() - primary->GetOriginVertexKineticEnergy());

        // Fill cut histograms looping over all MDs
        for(UInt_t oct = 1; oct < 9; oct ++)
        {
            // Cut:Total # of PEs > 0.0
            if(detector->GetDetectorID().size() > 0 && 
               detector->GetDetectorID()[oct] == (Int_t) oct && 
               pmt->GetPMTLeftNbOfPEs().size() > 0 &&
               pmt->GetPMTLeftNbOfPEs()[oct] > 1.0 &&
               pmt->GetPMTRightNbOfPEs().size() > 0 &&
               pmt->GetPMTRightNbOfPEs()[oct] > 1.0)
            {
                theta_cut_hist->Fill(TMath::Cos(primary->GetOriginVertexThetaAngle()*(TMath::Pi()/180.0)));
                phi_cut_hist->Fill(primary->GetOriginVertexPhiAngle());
                nu_cut_hist->Fill(primary->GetBeamEnergy() - 
                                  primary->GetOriginVertexKineticEnergy());
                theta_phi_cut_hist->Fill(TMath::Cos(primary->GetOriginVertexThetaAngle()*(TMath::Pi()/180.0)), primary->GetOriginVertexPhiAngle());
                theta_nu_cut_hist->Fill(TMath::Cos(primary->GetOriginVertexThetaAngle()*(TMath::Pi()/180.0)), primary->GetBeamEnergy() - primary->GetOriginVertexKineticEnergy());
                phi_nu_cut_hist->Fill(primary->GetOriginVertexPhiAngle(), primary->GetBeamEnergy() - primary->GetOriginVertexKineticEnergy());
            } // End if Total PEs check
        } // End of MD for loop

    } // End of for loop
}

TCanvas *Create_Canvas(const Char_t *name, Int_t num_x, Int_t num_y)
{
    // Generate Canvas for plots
    Double_t golden_mean = (TMath::Sqrt(5.0)-1.0)/2.0;
    Int_t width = 433; //[pt]
    Int_t height = (Int_t) width*golden_mean; //[pt]
    TCanvas * can = new TCanvas(name, name, num_x*width, num_y*height);
    can->Divide(num_x, num_y);
    return can;
}

void write_1d_data(Int_t nbins,
                   TH1D *theta_hist, 
                   TH1D *theta_cut_hist,
                   TH1D *phi_hist,
                   TH1D *phi_cut_hist,
                   TH1D *nu_hist,
                   TH1D *nu_cut_hist)
{
    // Write bin contents to file
    // Open file
    ofstream csv_file;
    csv_file.open("/u/home/kbartlet/Qweak/Al_Alloy_Sim/data/Al_Alloy_4p_DS_acceptance_1d_bins.csv", fstream::out | fstream::trunc);
    if(csv_file.is_open())
    {
        // Print Column headers
        csv_file << "bin_num," 
                 << "theta_x," 
                 << "theta_y,"
                 << "theta_cut_x,"
                 << "theta_cut_y,"
                 << "phi_x,"
                 << "phi_y,"
                 << "phi_cut_x,"
                 << "phi_cut_y,"
                 << "nu_x,"
                 << "nu_y,"
                 << "nu_cut_x,"
                 << "nu_cut_y" << endl;
        // Loop over bins
        for(Int_t bin = 1; bin < nbins+1; bin++)
        {
            csv_file << setprecision(5) << bin << "," 
                     << theta_hist->GetBinCenter(bin) << ","
                     << theta_hist->GetBinContent(bin) << ","
                     << theta_cut_hist->GetBinCenter(bin) << ","
                     << theta_cut_hist->GetBinContent(bin) << ","
                     << phi_hist->GetBinCenter(bin) << ","
                     << phi_hist->GetBinContent(bin) << ","
                     << phi_cut_hist->GetBinCenter(bin) << ","
                     << phi_cut_hist->GetBinContent(bin) << ","
                     << nu_hist->GetBinCenter(bin) << ","
                     << nu_hist->GetBinContent(bin) << ","
                     << nu_cut_hist->GetBinCenter(bin) << ","
                     << nu_cut_hist->GetBinContent(bin) << endl;
        } // End bin content for loop
        // Close .csv file
        csv_file.close();
    } // End if csv_file statement
    else
    {
        cerr << "!!! Warning: Error opening .csv file. !!!" << endl;
    }

    return;
}

void write_2d_data(const Char_t* label, Int_t nbins, TH2D* hist)
{
    //Write bin contents of two dimensional histogram to file
    //Open file
    ofstream csv_file;
    csv_file.open(Form("/u/home/kbartlet/Qweak/Al_Alloy_Sim/data/Al_Alloy_4p_DS_acceptance_2d_bins_%s.csv", label), fstream::out | fstream::trunc);
    if(csv_file.is_open())
    {
        // Loop over bins
        for(Int_t bin_y = 0; bin_y < nbins + 1; bin_y++)
        {
            for(Int_t bin_x = 0; bin_x < nbins + 1; bin_x++)
            {
                if(bin_y == 0)
                {
                    if(bin_x == 0)
                    {
                        csv_file << " ";
                    }
                    else
                    {
                        csv_file << "," << hist->GetXaxis()->GetBinCenter(bin_x);
                    }
                }
                else
                {
                    if(bin_x == 0)
                    {
                        csv_file << hist->GetYaxis()->GetBinCenter(bin_y);
                    }
                    else
                    {
                        csv_file << "," << hist->GetBinContent(bin_x, bin_y); 
                    }
                }
            } // End bin_j for loop
            csv_file << "\n";
        } // End bin_i for loop
        csv_file.close(); // Close .csv file
    } // End if csv file open
    else
    {
        cerr << "!!! Warning: Error opening 2d .csv file. !!!" << endl;
    }
    return;
}

# ifndef __CINT__
int main(Int_t argc, Char_t *argv[])
{
    // Check to make sure file sub-directory is given as input
    if(argc < 2)
    {
        cerr << "ROOT File sub-directory not passed to program!\n" <<
            "Try the following: >./Al_Alloy_Acceptance" << 
            " Al_Alloy_4p_DS_acceptance_run2" << endl;
    }
    Int_t fnum = 0; // Number of loaded files
    TChain * tree = Load_Files(argv[1], 101, 200, fnum);

    // Check if .root files loaded
    if(fnum > 0)
    {
        cout << "Number of files loaded: " << fnum << endl;
    }
    else
    {
        cerr << "!!! ERROR: No .root files loaded. !!!" << endl;
        return 0;
    }
   
    // Number of bins
    Int_t nbins = 100;
    // Initialize histograms
    TH1D *theta_hist = new TH1D("theta_hist", 
                                "", 
                                nbins, 
                                0.97, 
                                1.0);
    TH1D *theta_cut_hist = new TH1D("theta_cut_hist",
                                    "",
                                    nbins,
                                    0.97,
                                    1.0);
    TH1D *phi_hist = new TH1D("phi_hist",
                              "",
                              nbins,
                              -22.5,
                              22.5);
    TH1D *phi_cut_hist = new TH1D("phi_cut_hist",
                                  "",
                                  nbins,
                                  -22.5,
                                  22.5);
    TH1D *nu_hist = new TH1D("nu_hist",
                             "",
                             nbins,
                             0.0,
                             1200.0);
    TH1D *nu_cut_hist = new TH1D("nu_cut_hist",
                                 "",
                                 nbins,
                                 0.0,
                                 1200.0);
    TH2D *theta_phi_hist = new TH2D("theta_phi_hist",
                                    "",
                                    nbins,
                                    0.97,
                                    1.0,
                                    nbins,
                                    -22.5,
                                    22.5);
    TH2D *theta_phi_cut_hist = new TH2D("theta_phi_cut_hist",
                                        "",
                                        nbins,
                                        0.97,
                                        1.0,
                                        nbins,
                                        -22.5,
                                        22.5);
    TH2D *theta_nu_hist = new TH2D("theta_nu_hist",
                                   "",
                                   nbins,
                                   0.97,
                                   1.0,
                                   nbins,
                                   0.0,
                                   1200.0);
    TH2D *theta_nu_cut_hist = new TH2D("theta_nu_cut_hist",
                                       "",
                                       nbins,
                                       0.97,
                                       1.0,
                                       nbins,
                                       0.0,
                                       1200.0);
    TH2D *phi_nu_hist = new TH2D("phi_nu_hist",
                                 "",
                                 nbins,
                                 -22.5,
                                 22.5,
                                 nbins,
                                 0.0,
                                 1200.0);
    TH2D * phi_nu_cut_hist = new TH2D("phi_nu_cut_hist",
                                      "",
                                      nbins,
                                      -22.5,
                                      22.5,
                                      nbins,
                                      0.0,
                                      1200.0);

    // Loop over tree and fill histograms
    Loop_Tree(tree,
              theta_hist,
              phi_hist,
              nu_hist,
              theta_cut_hist,
              phi_cut_hist,
              nu_cut_hist,
              theta_phi_hist,
              theta_nu_hist,
              phi_nu_hist,
              theta_phi_cut_hist,
              theta_nu_cut_hist,
              phi_nu_cut_hist);

    // Create canvas for plots
    TCanvas *can_1d = Create_Canvas("can_1d", 2, 3);
    TCanvas *can_2d = Create_Canvas("can_2d", 2, 3);

    // Change style to remove name
    gStyle->SetOptStat("e");

    // Draw plots
    can_1d->cd(1);
    theta_hist->GetXaxis()->SetTitle("cos(#theta) []");
    theta_hist->GetXaxis()->CenterTitle();
    theta_hist->GetYaxis()->SetTitle("Entries");
    theta_hist->GetYaxis()->CenterTitle();
    theta_hist->SetLineColor(kBlue);
    theta_hist->Draw();

    can_1d->cd(2);
    theta_cut_hist->GetXaxis()->SetTitle("cos(#theta) []");
    theta_cut_hist->GetXaxis()->CenterTitle();
    theta_cut_hist->GetYaxis()->SetTitle("Entries");
    theta_cut_hist->GetYaxis()->CenterTitle();
    theta_cut_hist->SetLineColor(kBlue);
    theta_cut_hist->Draw();
    
    can_1d->cd(3);
    phi_hist->GetXaxis()->SetTitle("#phi [#circ]");
    phi_hist->GetXaxis()->CenterTitle();
    phi_hist->GetYaxis()->SetTitle("Entries");
    phi_hist->GetYaxis()->CenterTitle();
    phi_hist->SetLineColor(kBlue);
    phi_hist->Draw();

    can_1d->cd(4);
    phi_cut_hist->GetXaxis()->SetTitle("#phi [#circ]");
    phi_cut_hist->GetXaxis()->CenterTitle();
    phi_cut_hist->GetYaxis()->SetTitle("Entries");
    phi_cut_hist->GetYaxis()->CenterTitle();
    phi_cut_hist->SetLineColor(kBlue);
    phi_cut_hist->Draw();

    can_1d->cd(5);
    nu_hist->GetXaxis()->SetTitle("#nu [MeV]");
    nu_hist->GetXaxis()->CenterTitle();
    nu_hist->GetYaxis()->SetTitle("Entries");
    nu_hist->GetYaxis()->CenterTitle();
    nu_hist->SetLineColor(kBlue);
    nu_hist->Draw();

    can_1d->cd(6);
    nu_cut_hist->GetXaxis()->SetTitle("#nu [MeV]");
    nu_cut_hist->GetXaxis()->CenterTitle();
    nu_cut_hist->GetYaxis()->SetTitle("Entries");
    nu_cut_hist->GetYaxis()->CenterTitle();
    nu_cut_hist->SetLineColor(kBlue);
    nu_cut_hist->Draw();

    can_2d->cd(1);
    gPad->SetLogz();
    theta_phi_hist->GetXaxis()->SetTitle("cos(#theta) []");
    theta_phi_hist->GetXaxis()->CenterTitle();
    theta_phi_hist->GetYaxis()->SetTitle("#phi [#circ]");
    theta_phi_hist->GetYaxis()->CenterTitle();
    theta_phi_hist->GetZaxis()->SetTitle("Entries");
    theta_phi_hist->GetZaxis()->CenterTitle();
    theta_phi_hist->GetZaxis()->SetRangeUser(1e-1,1e3);
    theta_phi_hist->Draw("colZ");
    
    can_2d->cd(2);
    gPad->SetLogz();
    theta_phi_cut_hist->GetXaxis()->SetTitle("cos(#theta) []");
    theta_phi_cut_hist->GetXaxis()->CenterTitle();
    theta_phi_cut_hist->GetYaxis()->SetTitle("#phi [#circ]");
    theta_phi_cut_hist->GetYaxis()->CenterTitle();
    theta_phi_cut_hist->GetZaxis()->SetTitle("Entries");
    theta_phi_cut_hist->GetZaxis()->CenterTitle();
    theta_phi_cut_hist->GetZaxis()->SetRangeUser(1e-1,1e3);
    theta_phi_cut_hist->Draw("colZ");

    can_2d->cd(3);
    gPad->SetLogz();
    theta_nu_hist->GetXaxis()->SetTitle("cos(#theta) []");
    theta_nu_hist->GetXaxis()->CenterTitle();
    theta_nu_hist->GetYaxis()->SetTitle("#nu [MeV]");
    theta_nu_hist->GetYaxis()->CenterTitle();
    theta_nu_hist->GetZaxis()->SetTitle("Entries");
    theta_nu_hist->GetZaxis()->CenterTitle();
    theta_nu_hist->GetZaxis()->SetRangeUser(1e-1,1e3);
    theta_nu_hist->Draw("colZ");
    
    can_2d->cd(4);
    gPad->SetLogz();
    theta_nu_cut_hist->GetXaxis()->SetTitle("cos(#theta) []");
    theta_nu_cut_hist->GetXaxis()->CenterTitle();
    theta_nu_cut_hist->GetYaxis()->SetTitle("#nu [MeV]");
    theta_nu_cut_hist->GetYaxis()->CenterTitle();
    theta_nu_cut_hist->GetZaxis()->SetTitle("Entries");
    theta_nu_cut_hist->GetZaxis()->CenterTitle();
    theta_nu_cut_hist->GetZaxis()->SetRangeUser(1e-1,1e3);
    theta_nu_cut_hist->Draw("colZ");

    can_2d->cd(5);
    gPad->SetLogz();
    phi_nu_hist->GetXaxis()->SetTitle("#phi [#circ]");
    phi_nu_hist->GetXaxis()->CenterTitle();
    phi_nu_hist->GetYaxis()->SetTitle("#nu [MeV]");
    phi_nu_hist->GetYaxis()->CenterTitle();
    phi_nu_hist->GetZaxis()->SetTitle("Entries");
    phi_nu_hist->GetZaxis()->CenterTitle();
    phi_nu_hist->GetZaxis()->SetRangeUser(1e-1,1e3);
    phi_nu_hist->Draw("colZ");
    
    can_2d->cd(6);
    gPad->SetLogz();
    phi_nu_cut_hist->GetXaxis()->SetTitle("#phi [#circ]");
    phi_nu_cut_hist->GetXaxis()->CenterTitle();
    phi_nu_cut_hist->GetYaxis()->SetTitle("#nu [MeV]");
    phi_nu_cut_hist->GetYaxis()->CenterTitle();
    phi_nu_cut_hist->GetZaxis()->SetTitle("Entries");
    phi_nu_cut_hist->GetZaxis()->CenterTitle();
    phi_nu_cut_hist->GetZaxis()->SetRangeUser(1e-1,1e3);
    phi_nu_cut_hist->Draw("colZ");

    //Write 1d histogram data to .csv file
    write_1d_data(nbins,
                  theta_hist,
                  theta_cut_hist,
                  phi_hist,
                  phi_cut_hist,
                  nu_hist,
                  nu_cut_hist); 

    // Write 2d histograms data to .csv file
    write_2d_data("theta_phi",
                  nbins,
                  theta_phi_hist);
    write_2d_data("theta_phi_cut",
                  nbins,
                  theta_phi_cut_hist);
    write_2d_data("theta_nu",
                  nbins,
                  theta_nu_hist);
    write_2d_data("theta_nu_cut",
                  nbins,
                  theta_nu_cut_hist);
    write_2d_data("phi_nu",
                  nbins,
                  phi_nu_hist);
    write_2d_data("phi_nu_cut",
                  nbins,
                  phi_nu_cut_hist);

    // Save plots
    can_1d->SaveAs("/u/home/kbartlet/Qweak/Al_Alloy_Sim/plots/Al_Alloy_4p_DS_acceptance_1d.png");
    can_1d->SaveAs("/u/home/kbartlet/Qweak/Al_Alloy_Sim/plots/Al_Alloy_4p_DS_acceptance_1d.pdf");
    can_1d->SaveAs("/u/home/kbartlet/Qweak/Al_Alloy_Sim/plots/Al_Alloy_4p_DS_acceptance_1d.C");
    can_2d->SaveAs("/u/home/kbartlet/Qweak/Al_Alloy_Sim/plots/Al_Alloy_4p_DS_acceptance_2d.png");
    can_2d->SaveAs("/u/home/kbartlet/Qweak/Al_Alloy_Sim/plots/Al_Alloy_4p_DS_acceptance_2d.pdf");
    can_2d->SaveAs("/u/home/kbartlet/Qweak/Al_Alloy_Sim/plots/Al_Alloy_4p_DS_acceptance_2d.C");

    return 0;
}
# endif
